# Agoda Accomodation Recommendation

<a href="url"><img src="https://upload.wikimedia.org/wikipedia/en/c/cc/Agoda_mainlogo_stack_positive_ai_Main_Logo.jpg" height="250" width="500" ></a>

<p>This project aims to provide a list of accommodations recommendations from Agoda base on the features that the user prefers.

The raw dataset contains the availability of 300 accommodations for the month of November 2020. 

There are 7 types of accomodations found on Agoda:
- Resort
- Serviced apartment
- Hostel
- Capsule hotel
- Entire apartment
- Boat/cruise
- Resort villa

There are 25 types of features from which user can select their top 3 to rank the order of priority:
- Number of Stars
- Review Score
- Cleanliness
- Distance to Mall
- Distance to MRT
- Early Check-in (Before 3pm)
- Late Check-out (After 12pm)
- Pay Later
- Free Cancellation
- Gym
- Swimming Pool
- Car Park
- Airport Transfer
- Breakfast
- Hygiene+ (Covid-19)
- 24h Front Desk
- Laundry Service
- Bathtub
- Balcony
- Kitchen
- TV
- Internet
- Air Conditioning
- Ironing
- Non-Smoking

Base on the user's (1) date/s, (2) accomodation type/s and (3) weightage given to the top 3 features, the top 5 accomodations available will be listed.
The recommendations is generated based on the average accomodation features' score-to-price ratio.

Raw data is scrapeed from Agoda
Analysis and Dashboard are powered by Python and Dash
