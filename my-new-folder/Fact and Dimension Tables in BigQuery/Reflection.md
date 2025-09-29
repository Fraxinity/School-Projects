1. Why do we separate data into fact and dimension tables?
   
     It is interesting that we seperate fact table and dimension table when we can just make table in one go. The reason is simple, it's to make
     the information or data much more detailed to use. It improves data to be more less redundant and opening possibilities within the current data.
     Dimension tables help refine and structure the data in a way that supports the fact table. For example is that when making dimension table,
     we just extract the data and making it more refined to be used for the fact table.
2. What challenges might arise if we stored everything in one large table?

  There are a few possibilities but the main problem is that the data would be redundant and implicate poor performance for the data to be used. With 
  one large database would lead to a slow performance when analyzing data and will lead to missed opportunity for better insight of the data.
  This is the reason why we split our data to fact and dimensional tables. We explore the numerical side within the fact table while we analyze
  and extract posssible new information within the dimension table. Once everything is set, you can use a schema to join the two tables and make 
  analyzation way easier with new insights to be used and show.
