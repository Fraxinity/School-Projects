import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'your_secret_key_here'  # Replace with a unique, secret string

# Load the dataset
file_name = r'cleaned_okcupid_profiles.csv'
data = pd.read_csv(file_name)

# Encode categorical variables
categorical_columns = ['sex', 'orientation', 'status', 'body_type', 'diet', 'drinks', 'drugs', 'smokes']
label_encoders = {}

# Update the options for each category
options = {
    'status': ['single', 'available', 'seeing someone', 'married', 'unknown'],
    'sex': ['m', 'f'],
    'orientation': ['straight', 'bisexual', 'gay'],
    'body_type': ['a little extra', 'average', 'thin', 'athletic', 'fit', 'nan', 'skinny', 'curvy', 
                  'full figured', 'jacked', 'rather not say', 'used up', 'overweight'],
    'diet': ['strictly anything', 'mostly other', 'anything', 'vegetarian', 'nan', 'mostly anything',
             'mostly vegetarian', 'strictly vegan', 'strictly vegetarian', 'mostly vegan', 'strictly other', 
             'mostly halal', 'other', 'vegan', 'mostly kosher', 'strictly halal', 'halal', 'strictly kosher', 'kosher'],
    'drinks': ['socially', 'often', 'not at all', 'rarely', 'nan', 'very often', 'desperately'],
    'drugs': ['never', 'sometimes', 'nan', 'often'],
    'smokes': ['sometimes', 'no', 'nan', 'when drinking', 'yes', 'trying to quit']
}

# Encode categorical variables based on updated options
for col in categorical_columns:
    if col in data.columns:
        label_encoders[col] = LabelEncoder()
        label_encoders[col].fit(options[col])
        data[col] = label_encoders[col].transform(data[col].astype(str))

# Select features for matchmaking
features = ['age', 'sex', 'orientation', 'status', 'body_type', 'diet', 'drinks', 'drugs', 'smokes']
X = data[features]

# Fill missing values with median for numeric columns
X = X.fillna(X.median())

# Standardize features for regression
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create a mock "random match score" for training
data['random_match_score'] = np.random.rand(len(data))  # Fake target for demonstration
y = data['random_match_score']

# Train a linear regression model
model = LinearRegression()
model.fit(X_scaled, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_matches', methods=['POST'])
def find_matches():
    # Get user input from the form
    age = int(request.form['age'])
    sex = request.form['sex']
    orientation = request.form['orientation']
    status = request.form['status']
    body_type = request.form['body_type']
    diet = request.form['diet']
    drinks = request.form['drinks']
    drugs = request.form['drugs']
    smokes = request.form['smokes']
    preferred_sex = request.form['preferred_sex']
    preferred_orientation = request.form['preferred_orientation']
    age_min = int(request.form['age_min'])
    age_max = int(request.form['age_max'])

    # Encode user input
    user_input = {
        'age': age,
        'sex': sex,
        'orientation': orientation,
        'status': status,
        'body_type': body_type,
        'diet': diet,
        'drinks': drinks,
        'drugs': drugs,
        'smokes': smokes
    }

    for col in categorical_columns:
        if col in user_input and col in label_encoders:
            user_input[col] = label_encoders[col].transform([user_input[col]])[0]
    
    # Create a DataFrame for the user input
    user_input_df = pd.DataFrame([user_input])

    # Standardize user input using the scaler
    user_input_scaled = scaler.transform(user_input_df)

    # Filter dataset based on the preferred sex, preferred orientation, and age range
    preferred_sex_encoded = label_encoders['sex'].transform([preferred_sex])[0]
    preferred_orientation_encoded = label_encoders['orientation'].transform([preferred_orientation])[0]
    
    filtered_data = data[(
        (data['sex'] == preferred_sex_encoded) & 
        (data['orientation'] == preferred_orientation_encoded) & 
        (data['age'] >= age_min) & 
        (data['age'] <= age_max)
    )]

    # Predict match scores for filtered users
    filtered_X_scaled = scaler.transform(filtered_data[features])
    filtered_data['model_match_score'] = model.predict(filtered_X_scaled)

    # Calculate match compatibility percentage
    user_model_score = model.predict(user_input_scaled)[0]
    filtered_data['match_compatibility'] = 100 - (abs(filtered_data['model_match_score'] - user_model_score) * 100)

    # Sort by compatibility in descending order (best matches first)
    filtered_data = filtered_data.sort_values(by='match_compatibility', ascending=False)

    # Get top 5 matches
    top_matches = filtered_data.head(100)

    # Prepare matches data for display
    matches = []
    for _, match in top_matches.iterrows():
        matches.append({
            'id': match.name,  # Displaying the ID (row number) for each match
            'row_number': match.name,  # Row number for display
            'age': match['age'],
            'sex': label_encoders['sex'].inverse_transform([int(match['sex'])])[0],
            'orientation': label_encoders['orientation'].inverse_transform([int(match['orientation'])])[0],
            'status': label_encoders['status'].inverse_transform([int(match['status'])])[0],
            'body_type': label_encoders['body_type'].inverse_transform([int(match['body_type'])])[0],
            'diet': label_encoders['diet'].inverse_transform([int(match['diet'])])[0],
            'drinks': label_encoders['drinks'].inverse_transform([int(match['drinks'])])[0],
            'drugs': label_encoders['drugs'].inverse_transform([int(match['drugs'])])[0],
            'smokes': label_encoders['smokes'].inverse_transform([int(match['smokes'])])[0],
            'match_compatibility': round(match['match_compatibility'], 2)
        })

    # Save the matches in the session for pagination
    session['matches'] = matches
    session['current_match_index'] = 0

    return redirect(url_for('show_match'))

@app.route('/show_match')
#Shows your matches
def show_match():
    matches = session.get('matches', [])
    current_index = session.get('current_match_index', 0)

    if current_index < len(matches):
        match = matches[current_index]
        return render_template('results.html', match=match)

    return render_template('results.html', match=None, message="No more matches available.")

@app.route('/next_match')
#Gets your next matches based on the percentage
def next_match():
    matches = session.get('matches', [])
    current_index = session.get('current_match_index', 0)

    if current_index + 1 < len(matches):
        session['current_match_index'] = current_index + 1
        return redirect(url_for('show_match'))

    return render_template('results.html', match=None, message="No more matches available.")

if __name__ == '__main__':
    app.run(debug=True)

