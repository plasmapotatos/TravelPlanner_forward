import langfun as lf
import pyglove as pg
import os

from utils.travel_planner_class import Day
from agents.prompts import langfun_day_by_day_agent_prompt, langfun_planner_agent_prompt

def query_langfun(query):
    while(True):
        try:
            return lf.query(query, list[Day], lm=lf.llms.Gpt4Turbo(), examples=[
                # lf.MappingExample(input='1 + 1', output=2, schema=int, preamble='Give me OUTPUT_OBJECT.')
                lf.MappingExample(input='1 + 1', output=2, schema=int)
            ])
        except Exception as e:
            print(e)
            continue

def get_number_of_days(query):
    while(True):
        try:
            return lf.query("How many days is the following request wanting?\n" + query, int, lm=lf.llms.Gpt4Turbo(), examples=[
                # lf.MappingExample(input='1 + 1', output=2, schema=int, preamble='Give me OUTPUT_OBJECT.')
                lf.MappingExample(input='1 + 1', output=2, schema=int)
            ])
        except Exception as e:
            print(e)
            continue

def langfun_request_by_day(text, query):
    current_state = []
    total_cost = 0.0
    num_days = get_number_of_days(query)
    for i in range(num_days):
        while(True):
            try:
                prompt = langfun_day_by_day_agent_prompt.format(reference_information=text, query=query, current_state=current_state)
                next_day = lf.query(prompt, Day, lm=lf.llms.Gpt4Turbo(), examples=[
                    # lf.MappingExample(input='1 + 1', output=2, schema=int, preamble='Give me OUTPUT_OBJECT.')
                    lf.MappingExample(input='1 + 1', output=2, schema=int)
                ])
                break
            except Exception as e:
                print(e)
                continue
        current_state.append(next_day)
        # if next_day.breakfast is not None:
        #     total_cost += next_day.breakfast.cost
        # if next_day.lunch is not None:
        #     total_cost += next_day.lunch.cost
        # if next_day.dinner is not None:
        #     total_cost += next_day.dinner.cost
        # if next_day.accommodation is not None:
        #     total_cost += next_day.accomodation.cost
    return current_state

if(__name__ == '__main__'):
    query = langfun_request_by_day("""Please help me plan a trip from St. Petersburg to Rockford spanning 3 days from March 16th to March 18th, 2022. The travel should be planned for a single person with a budget of $1,700.
                        USe the following reference information: [{'Description': 'Attractions in Rockford', 'Content': " Name Latitude Longitude Address Phone Website City\n Burpee Museum of Natural History 42.277324 -89.088142 737 N Main St, Rockford, IL 61103, USA (815) 965-3433 http://www.burpee.org/ Rockford\n Midway Village Museum 42.280499 -88.984640 6799 Guilford Rd, Rockford, IL 61107, USA (815) 397-9112 https://www.midwayvillage.com/ Rockford\n Discovery Center Museum 42.277105 -89.089430 711 N Main St, Rockford, IL 61103, USA (815) 963-6769 http://www.discoverycentermuseum.org/ Rockford\nTinker Swiss Cottage Museum and Gardens 42.264110 -89.102796 411 Kent St, Rockford, IL 61102, USA (815) 964-2424 http://www.tinkercottage.com/ Rockford\n Anderson Japanese Gardens 42.290054 -89.057795 318 Spring Creek Rd, Rockford, IL 61107, USA (815) 229-9390 http://andersongardens.org/ Rockford\n Nicholas Conservatory & Gardens 42.282293 -89.070704 1354 N 2nd St, Rockford, IL 61107, USA (815) 987-8858 http://www.nicholasconservatory.com/ Rockford\n Erlander Home Museum 42.264098 -89.088693 404 S 3rd St, Rockford, IL 61104, USA (815) 963-5559 http://www.swedishhistorical.org/ Rockford\n Ethnic Heritage Museum 42.261100 -89.100915 1129 S Main St, Rockford, IL 61101, USA (815) 962-7402 https://www.ethnicheritagemuseum.org/ Rockford\n Sinnissippi Park 42.282729 -89.064116 1401 N 2nd St, Rockford, IL 61107, USA (815) 987-8858 http://rockfordparkdistrict.org/ncg Rockford\n Klehm Arboretum & Botanic Garden 42.244452 -89.112540 2715 S Main St, Rockford, IL 61102, USA (815) 965-8146 http://www.klehm.org/ Rockford\n Davis Park at Founders Landing 42.268250 -89.095379 320 S Wyman St, Rockford, IL 61101, USA (815) 968-5600 https://www.gorockford.com/listings/davis-park-at-founders-landing/275/ Rockford\n Frank Lloyd Wright's Laurent House 42.299833 -89.024362 4646 Spring Brook Rd, Rockford, IL 61114, USA (815) 877-2952 http://www.laurenthouse.com/ Rockford\n Sinnissippi Gardens 42.284031 -89.067901 1354 N 2nd St, Rockford, IL 61107, USA (815) 987-8858 https://nicholasconservatory.com/ Rockford\n Riverfront Museum Park 42.276843 -89.088859 Ste 3, 711 N Main St, Rockford, IL 61103, USA (815) 962-0105 Unknown Rockford\n Searls Park 42.300685 -89.124144 4950 Safford Rd, Rockford, IL 61101, USA (815) 987-8800 http://rockfordparkdistrict.org/ Rockford\n La Paloma Gardens 42.293671 -89.034617 3622 Brookview Rd, Rockford, IL 61107, USA (815) 399-0324 http://www.lapalomagardens.com/ Rockford\n Rockford Park District 42.268422 -89.097234 401 S Main St, Rockford, IL 61101, USA (815) 987-8800 https://rockfordparkdistrict.org/ Rockford\n Aldeen Park 42.274060 -89.022769 623 N Alpine Rd, Rockford, IL 61107, USA Unknown https://www.rockfordparkdistrict.org/ Rockford\n Blackhawk Springs Forest Preserve 42.204694 -88.991636 5360 Mulford Road &, 5801 Perryville Rd, Rockford, IL 61109, USA (815) 877-6100 http://winnebagoforest.org/preserves/blackhawk-springs/ Rockford\n Ingersoll Centennial Park 42.266298 -89.091439 315 S 1st St, Rockford, IL 61104, USA (815) 987-8800 http://rockfordparkdistrict.org/ Rockford"}, {'Description': 'Restaurants in Rockford', 'Content': " Name Average Cost Cuisines Aggregate Rating City\n39 Coco Bambu 72 Tea, French, Bakery, BBQ, Cafe 4.9 Rockford\n251 Flying Mango 20 American, BBQ, Seafood 4.5 Rockford\n2470 Gajalee Sea Food 49 Bakery, BBQ 3.9 Rockford\n2861 Shree Balaji Chaat Bhandar 97 French, Bakery, BBQ, Italian 3.2 Rockford\n3052 Moets Arabica 43 Tea, Bakery, Indian, Fast Food 3.5 Rockford\n3163 Cafe Coffee Day 28 Chinese, Desserts, Pizza, Cafe, Mediterranean 0.0 Rockford\n3700 Nutri Punch 34 Tea, Chinese, Cafe, Desserts 4.0 Rockford\n4319 Cafe Southall 56 Seafood, Pizza, Cafe, Fast Food 4.2 Rockford\n4348 Eggspectation - Jaypee Vasant Continental 77 Tea, Mediterranean, Seafood 3.6 Rockford\n4542 Aroma Rest O Bar 58 Bakery, Fast Food, Chinese, American, Seafood 3.6 Rockford\n4735 Advance Bakery 100 Desserts, Pizza, Mexican, Bakery, Chinese, Seafood 2.9 Rockford\n4789 Dial A Cake 29 Cafe, American, Mediterranean, Desserts 0.0 Rockford\n5309 U Like 32 Tea, French, Desserts 0.0 Rockford\n5459 Subway 42 Tea, Chinese, Pizza 3.4 Rockford\n5661 Aggarwal Sweet Centre 81 Desserts, Tea, Italian, Bakery, Cafe 0.0 Rockford\n6078 Aggarwal Sweets Centre 73 Fast Food, Chinese, BBQ, Italian 0.0 Rockford\n6313 Giri Momos Centre & Chinese Fast Food 44 Cafe, Indian, Seafood 2.4 Rockford\n6388 Mr. Confectioner - Pride Plaza Hotel 74 Bakery, Desserts 0.0 Rockford\n6507 Faaso's 98 Bakery, Desserts, Seafood 0.0 Rockford\n6796 Hangchuaa's Chinese Food Corner 64 Tea, BBQ, Seafood 3.1 Rockford\n7295 Grappa - Shangri-La's - Eros Hotel 21 Bakery, Desserts, Italian 3.4 Rockford\n7955 New Bhappe Di Hatti 76 Seafood, Mexican, BBQ, Fast Food 0.0 Rockford\n8095 Dunkin' Donuts 24 Cafe, Bakery, BBQ, Seafood 0.0 Rockford\n8455 Subway 26 Bakery, Pizza, BBQ, Desserts 3.8 Rockford\n8821 The Gourmet Shack 77 Tea, Pizza, Indian, Fast Food 3.3 Rockford\n8844 Mirchievous 64 American, Indian, BBQ, Seafood 3.1 Rockford\n9340 Chaophraya 74 Chinese, Pizza, Cafe, Desserts 3.9 Rockford"}, {'Description': 'Accommodations in Rockford', 'Content': ' NAME price room type house_rules minimum nights maximum occupancy review rate number city\n Spacious 3BDR Prime Location! 1030.0 Entire home/apt No smoking 2.0 9 2.0 Rockford\n Private Room in a two bedroom apt. 210.0 Private room No visitors & No smoking 1.0 2 4.0 Rockford\n Private rooms And Matchless Location 1075.0 Private room No pets & No parties 2.0 2 2.0 Rockford\nPark Side Zen Home - Terrace & next to CentralPark 250.0 Entire home/apt No children under 10 3.0 3 3.0 Rockford\n Lux 2 Bedroom NYC Apt on the Hudson River! 737.0 Entire home/apt No smoking 30.0 4 5.0 Rockford\n Modern 1-bedroom apartment in Fordham 377.0 Entire home/apt No pets 7.0 2 5.0 Rockford\n Private bedroom in BedStuy! 1107.0 Private room No smoking 10.0 1 4.0 Rockford\n Pure luxury one bdrm + sofa bed on Central Park 243.0 Entire home/apt No smoking & No parties 2.0 3 3.0 Rockford\n Charming studio in the heart of Astoria 519.0 Entire home/apt No parties 4.0 4 4.0 Rockford\n The heart of Brooklyn 154.0 Entire home/apt No children under 10 & No visitors & No pets 30.0 3 2.0 Rockford\n Private Stuyvesant Bedroom Madison 1R-2 395.0 Private room No parties & No children under 10 30.0 2 3.0 Rockford\n Sunny big bedroom in lively Brooklyn neighborhood 440.0 Private room No pets & No smoking 14.0 2 3.0 Rockford\n Midtown 2 Bed United Nations Loc, Full Kitchen 245.0 Entire home/apt No visitors 3.0 3 4.0 Rockford'}, {'Description': 'Flight from St. Petersburg to Rockford on 2022-03-16', 'Content': 'Flight Number Price DepTime ArrTime ActualElapsedTime FlightDate OriginCityName DestCityName Distance\n F3573659 474 15:40 17:04 2 hours 24 minutes 2022-03-16 St. Petersburg Rockford 1049.0'}, {'Description': 'Self-driving from St. Petersburg to Rockford', 'Content': 'No valid information.'}, {'Description': 'Taxi from St. Petersburg to Rockford', 'Content': 'No valid information.'}, {'Description': 'Flight from Rockford to St. Petersburg on 2022-03-18', 'Content': 'Flight Number Price DepTime ArrTime ActualElapsedTime FlightDate OriginCityName DestCityName Distance\n F3573120 346 19:00 22:43 2 hours 43 minutes 2022-03-18 Rockford St. Petersburg 1049.0'}, {'Description': 'Self-driving from Rockford to St. Petersburg', 'Content': 'No valid information.'}, {'Description': 'Taxi from Rockford to St. Petersburg', 'Content': 'No valid information.'}]""")
    print(query)