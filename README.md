# TravelAgent

## Prerequisites:
Python 3.10+ (3.12 recommended)

## Setup:

#### 1) Clone and enter the repo
git clone https://github.com/JonathanZmora/TravelAgent

cd TravelAgent

#### 2) Create a virtual env
python -m venv venv

#### 3) Activate the virtual env
**on macOS/Linux**: source ./venv/bin/activate

**on Windows**: .\venv\Scripts\activate

#### 4) Install dependencies
pip install -r requirements.txt

#### 5) Run
python main.py


## Key prompt engineering decisions:

**1. Multi-step reasoning prompt (chain-of-thought):**
   
   The REASONING_STEPS prompt guides the model through:
   
   (1) intent -> (2) required info -> (3) tool selection -> (4) blend tool output → (5) validate.
   
   These steps ensure that the assistant generates a relevant and helpful answer,
   
   asks for the information it needs and limits hallucinations.
   

**2. Clear tool policy by intent:**
 
   The "weather tool policy" section in the system prompt ensures the assistant know how and when to call the weather tool.
   
   The general rules are:
   
   a. Destination recommendations: never call weather tool (use seasonal knowledge).
      
   b. Packing or Local attractions: call weather only if dates are within the next 8 days and destination is known.
      
   The logic behind this policy is that we don't need to know the exact weather to recommend a destination because the llm
   
   knows what the probable weather is if given the location and dates.
   
   Also, the weather forecast from the OpenWeatherMap API is only for the next 8 days, so beyond that we also rely on llm knowledge.
   
   This policy removes ambiguity and prevents wasteful and invalid tool calls.
   

**3. Few-shot Examples**
   
   Short examples (one per intent) to stabilize tone, structure, and tool selection while keeping outputs concise and actionable.


## Sample conversation transcripts:

**EXAMPLE 1 (with internal reasoning):**

**You:** I’ve got a 4-day weekend in mid-October. I want somewhere warm and walkable. Ideas?

**Assistant:**

Reasoning:
- Intent: destination recommendations
- Dates and departure city missing
- Provide warm and walkable options with consideration for mid-October weather
- Ask for departure city and exact dates to refine

Final Answer:

For a warm and walkable 4-day weekend in mid-October, consider:
- Seville, Spain: Warm autumn days, rich history, and walkable Santa Cruz neighborhood
- New Orleans, Louisiana: Mild October weather, vibrant French Quarter, and scenic riverfront
- Charleston, South Carolina: Charming historic district, pleasant fall weather, and nearby beaches
- Barcelona, Spain: Mild Mediterranean climate, iconic architecture, and stroll-friendly Gothic Quarter

Quick tips:
- Book accommodations in central, walkable areas to minimize transit time
- Check local event calendars for festivals or holidays that might interest you

Suggested follow-ups: What city are you departing from, and are there any specific activities or cultural experiences you're looking for?

**You:** I'm departing from Tel Aviv, and I would like to go on a hike also

**Assistant:**

Reasoning:
- Intent: destination recommendations
- Departure city: Tel Aviv
- Added preference: hiking
- Consider destinations with warm weather, walkability, and accessible hiking trails
- Refine options based on flight duration and convenience from Tel Aviv

Final Answer:

Considering your departure from Tel Aviv and desire for a warm, walkable destination with hiking opportunities, here are some refined options:
- Cyprus: Only an hour's flight from Tel Aviv, Cyprus offers warm October weather, beautiful beaches, and scenic hiking trails in the Troodos Mountains
- Crete, Greece: A 1.5-hour flight from Tel Aviv, Crete has a mild Mediterranean climate, charming old towns, and stunning hiking trails like the Samaria Gorge
- Rhodes, Greece: Another 1.5-hour flight from Tel Aviv, Rhodes offers a warm autumn climate, a UNESCO-listed medieval town, and scenic hiking trails along the island's coastline
- Jordan (Aqaba or Petra): Approximately a 1-hour flight from Tel Aviv, Jordan offers warm weather, historic sites like Petra, and hiking opportunities in the Jordan Trail or Wadi Rum desert

Quick tips:
- Research hiking trail conditions and difficulty levels before your trip
- Consider guided hikes or join local hiking groups for a more immersive experience

Suggested follow-ups: Are you open to more off-the-beaten-path destinations, or do you prefer well-touristed areas with established hiking infrastructure?


**EXAMPLE 2 (without internal reasoning):**

**You:** I’m traveling hand-luggage only to somewhere rainy this weekend.

**Assistant:**

I didn't quite get the location. For packing suggestions, I need to know the destination. Can you please tell me where you're headed this weekend?

**You:** I'm traveling to Koh Tao

**Assistant:**

Based on the forecast, it seems like you can expect light rain and overcast clouds during your trip to Koh Tao this weekend, with temperatures ranging from 27-29°C.

For hand-luggage-only travel to a rainy destination, here are some essentials to pack:
- Lightweight and quick-drying clothing (e.g., 2-3 tops, 2 bottoms)
- Waterproof or water-resistant jacket or poncho
- Swimwear (for snorkeling or diving, if applicable)
- Undergarments and socks
- Comfortable walking shoes or sandals with a good grip
- Travel-sized toiletries
- Power bank for your phone or other devices
- Reef-safe sunscreen
- Insect repellent
- Travel documents (passport, ID, etc.)

Considering the rain, you may also want to pack:
- A compact umbrella
- Waterproof phone case or bag
- Quick-dry travel towel

Suggested follow-ups: Are you planning any specific activities like snorkeling or diving? Do you have any preferred clothing items or personal care products you'd like to pack?

**You:** I want to do activities but I don't know what. Can you recommend some?

**Assistant**:

Koh Tao is a beautiful island with plenty of activities to enjoy. Considering the rainy weather, here are some recommendations:
- Snorkeling or diving: Explore the underwater world of Koh Tao, known for its vibrant coral reefs and diverse marine life. Many dive sites are suitable for beginners, and the rain shouldn't affect the water conditions.
- Island hiking: Put on your hiking shoes and discover the island's scenic trails, which offer stunning views of the surrounding waters and lush forests.
- Rock climbing: For the more adventurous, Koh Tao has several rock climbing routes with breathtaking views of the island and the sea.
- Yoga or wellness: Take a moment to relax and rejuvenate with a yoga class or a spa treatment, perfect for a rainy day.
- Cooking class: Learn about Thai cuisine and cooking techniques with a local class, where you can discover the flavors and ingredients of the region.

Keep in mind that some outdoor activities might be affected by the rain, so it's a good idea to check with local operators for updates and advice.

Suggested follow-ups: Are you interested in any water activities, or would you prefer to stay on land? Do you have any experience with snorkeling, diving, or rock climbing?
