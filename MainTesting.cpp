#include <iostream>
#include "Modular/Cookielator.h"
using namespace std;

int main(){

    double num1, num2, result;
    int choice;

    cout << "Cookielator" << endl;

    do{
        cout << "1. Addition +" << endl;
        cout << "2. Subtraction -" << endl;
        cout << "3. Multiplication *" << endl;
        cout << "4. Division /" << endl;
        cout << "5. Exit" << endl;
        cout << "Choose options between 1-5: ";
        cin >> choice;

        if (choice >=1 && choice <=4){
            cout << "Enter the first number: ";
            cin >> num1;
            cout << "Enter the second number: ";
            cin >> num2;

            switch (choice){
                case 1:
                    result = add(num1, num2);
                    cout << num1 << "+" << num2 << "=" << result << endl;
                    break;
                case 2:
                    result = sub(num1, num2);
                    cout << num1 << "-" << num2 << "=" << result << endl;
                    break;
                case 3:
                    result = mul(num1, num2);
                    cout << num1 << "*" << num2 << "=" << result << endl;
                    break;
                case 4:
                    result = div(num1, num2);
                    cout << num1 << "/" << num2 << "=" << result << endl;
                    break;
            }
        } else if (choice == 5){
            cout << "Goodbye" << endl;
        } else{
            cout << "Invalid number. Try a different number" << endl;
        }
    } while (choice != 5);

    return 0;

}