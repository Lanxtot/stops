# Imports

import re
import requests
import csv
import os
from datetime import datetime
from zipfile import ZipFile

# Files

os_file = 'os.txt'
stops_file = 'stops_list.csv'
departures_file = 'departures.csv'
gps_file = 'gps_data.csv'
models_file_1 = 'models.csv'
models_file_2 = 'models_short.csv'
regional_models_file = 'models_regional.csv'
challenge_file = 'challenge.csv'
ridango_stops_file = 'stops.csv'
schedule_file = 'schedule_types.csv'
exceptions_file = 'exceptions.csv'
favorites_file = 'favorites.csv'
bugs_file = 'bugs.txt'
date_file = 'date.txt'

# Mini functions

def error():
    print('Prašome patikslinti.')

def connection():
    print('Patikrinkite interneto ryšį.')

def normalize(input_string):
    # Dictionary to map Lithuanian characters to their English equivalents
    char_map = {
        'ą': 'a', 'č': 'c', 'ę': 'e', 'ė': 'e', 'į': 'i', 'š': 's', 'ų': 'u', 'ū': 'u', 'ž': 'z'
    }

    # Capitalize the entire string first
    input_string = input_string.upper()

    # Replace Lithuanian characters with their English equivalents
    for lith_char, eng_char in char_map.items():
        input_string = input_string.replace(lith_char.upper(), eng_char.upper())
        input_string = input_string.replace(lith_char.lower(), eng_char.lower())

    # Remove non-alphabetical characters (keeping only letters)
    cleaned_string = re.sub(r'[^a-zA-Z]', '', input_string)
    return cleaned_string

def rip_txt(url,selected_file):
    response = requests.get(url)
    response.encoding = 'utf-8'

    with open(selected_file, 'w', encoding='utf-8') as file14:
        file14.write(response.text)

def current_time():
    with open(os_file, 'r') as os_data_4:
        if os_data_4.read() == '3':
            now = datetime.now()
            hours = (now.hour + 2) % 24
            minutes = now.minute
            seconds = now.second
            return f'{hours:02}:{minutes:02}:{seconds:02}'
        else:
            return datetime.now().strftime('%H:%M:%S')

def rip_from_zipfile(gtfs_file):
    # Define filenames
    local_zip_filename = "gtfs.zip"

    # Download the GTFS file
    response = requests.get(gtfs_file)
    response.raise_for_status()

    # Save the downloaded file locally
    with open(local_zip_filename, "wb") as f:
        f.write(response.content)

    # Extract the specified files
    with ZipFile(local_zip_filename, "r") as zf:
        for file_name in ["stops.txt"]:
            if file_name in zf.namelist():
                zf.extract(file_name, os.getcwd())

                # Rename .txt files to .csv
                base_name, ext = os.path.splitext(file_name)
                new_name = f"{base_name}.csv"

                if os.path.exists(new_name):
                    os.remove(new_name)
                os.rename(file_name, new_name)

    # Clean up the downloaded zip file
    if os.path.exists(local_zip_filename):
        os.remove(local_zip_filename)

# Main features

def match_entered_stop(entered_stop):
    rip_txt("https://www.stops.lt/vilnius/vilnius/stops.txt", stops_file)

    partial_matches = {}
    last_non_empty_value = None
    updated_rows = []
    normalized_entered_stop = normalize(entered_stop)  # Normalize the user input once

    # Load valid values from the second column of ridango_stops_file
    valid_values = set()
    with open(ridango_stops_file, mode='r', encoding='utf-8') as ridango_file:
        ridango_reader = csv.reader(ridango_file, delimiter=',')
        for row in ridango_reader:
            valid_values.add(row[1].strip())

    with open(stops_file, mode='r', encoding='utf-8') as file1:
        file1_csv_reader = csv.reader(file1, delimiter=';')

        for row_number, row in enumerate(file1_csv_reader, start=1):

            # Ensure the row has at least 8 columns
            while len(row) <= 7:
                row.append('')  # Add empty values until the row has at least 8 columns

            # Handle the 6th column (index 5)
            if row[5]:
                last_non_empty_value = row[5]
            else:
                row[5] = last_non_empty_value  # Use the value from the previous row if 6th column is empty

            # Skip rows whose first column does not match any value in valid_values
            if row[0] not in valid_values:
                updated_rows.append(row)  # Add skipped row without modification
                continue

            # Handle the 8th column (index 7)
            if not row[7]:
                # If 8th column is empty, fill it with the previous row value and chain them
                if row_number > 1:
                    prev_row = updated_rows[-1] if updated_rows else None
                    if prev_row and prev_row[7]:
                        row[7] = prev_row[7] + " " + row[7]  # Chain the previous and current 8th column values

            original_value = row[5]  # Get the original value (with spaces)
            normalized_value = normalize(original_value)  # Normalize the value (removes special chars but keeps spaces)

            # Check if the user input appears at the start of any word in the stop name
            words = original_value.split()  # Split the original value into words to preserve spaces

            for word in words:
                # Normalize the word and check if it starts with the normalized user input
                if normalize(word).startswith(normalized_entered_stop):
                    partial_matches[row_number] = original_value
                    break  # Exit the loop once a match is found

            if normalized_value.startswith(normalized_entered_stop):
                partial_matches[row_number] = original_value

            updated_rows.append(row)

    # After processing the file, rewrite it with the updated rows
    with open(stops_file, mode='w', encoding='utf-8', newline='') as file13:
        csv_writer = csv.writer(file13, delimiter=';')
        csv_writer.writerows(updated_rows)

    return partial_matches

def handle_partial_matches(partial_matches):
    # Extract the values from the dictionary (the 6th column values)
    values = list(partial_matches.values())
    
    # Dismiss any matches containing 'išlaipinimas' or 'atstova' (case-insensitive)
    dismissed_values = [value for value in values if 'išlaipinimas' in value.lower() or 'išlaipinama' in value.lower() or 'atstova' in value.lower() or 'atstovos' in value.lower()]
    
    for k in partial_matches:
        if partial_matches[k] == 'Kirtimų geležinkelio stotis':
            partial_matches[k] = 'Stotis'
    
    # Remove dismissed matches from the partial matches
    partial_matches = {k: v for k, v in partial_matches.items() if v not in dismissed_values}

    # Check if all values are the same
    if len(set(partial_matches.values())) == 1:
        # Gather rows that match the stop_name
        stop_name = list(partial_matches.values())[0]  # You can still use the stop_name if you need it
        stop_directions_rows = [row_number for row_number, value in partial_matches.items() if value == stop_name]
        return stop_directions_rows, stop_name  # Return both the list of rows and the selected stop name

    
    # If the values are different, handle accordingly
    unique_values = list(set(partial_matches.values()))  # Get the unique values
    if len(unique_values) >= 10:
        print('Susiaurinkite paiešką.')
        return None, None
    if len(unique_values) == 0:
        print('Nėra atitikmenų.')
        return None, None  # Indicating that the user needs to retry (this will trigger restart in main)
    
    # If there are less than 10 unique values, sort them alphabetically and print them
    unique_values.sort()  # Sorting the unique values alphabetically
    for idx, value in enumerate(unique_values, start=1):
        print(f"  {idx}: {value}")

    # Prompt user to select an option
    selection = input("Nr.: ")

    while True:
        try:
            user_choice = int(selection)  # Get user's choice
            if 1 <= user_choice <= len(unique_values):
                stop_name = unique_values[user_choice - 1]  # Adjust index for selection
                # Gather rows that match the selected stop_name
                stop_directions_rows = [row_number for row_number, value in partial_matches.items() if value == stop_name]
                return stop_directions_rows, stop_name  # Return both the list of rows and the selected stop name
            else:
                error()  # Invalid choice, prompt again
        except:
            if not selection:
                return None, None
            else:
                error()

def determine_stop_direction(stop_name, stop_directions_rows):
    # Read the exceptions.csv file and create a dictionary with Code and Option
    exceptions = {}
    with open(exceptions_file, mode='r', encoding='utf-8') as file2:
        file2_csv_reader = csv.DictReader(file2, delimiter=';')
        for row in file2_csv_reader:
            exceptions[row['Code']] = row['Direction']

    # Open the main CSV file and read it once to store all rows
    with open(stops_file, mode='r', encoding='utf-8') as file3:
        file3_csv_reader = csv.reader(file3, delimiter=';')
        rows = list(file3_csv_reader)  # Store all rows in a list

    # Create a mapping of directions to their respective 7th and 8th column values
    direction_7th_column = {
        row_number: rows[row_number - 1][6].strip()  # 7th column (indexed at 6)
        for row_number in stop_directions_rows
    }

    direction_8th_column = {
        row_number: rows[row_number - 1][7].strip()  # 8th column is at index 7
        for row_number in stop_directions_rows
    }

    # Collect directions from the specified rows in the main CSV
    directions = {
        row_number: rows[row_number - 1][1]  # 2nd column is the direction
        for row_number in stop_directions_rows
    }

    # Create a list of directions with the necessary modifications for laikina
    displayed_directions = []

    for row_number, direction in directions.items():
        direction_7th = direction_7th_column[row_number]  # Get the 7th column value
        direction_2nd = rows[row_number - 1][1].strip()  # Get the 2nd column value (direction)
        code_1st = rows[row_number - 1][0].strip()  # 1st column value (Code)

        if code_1st in exceptions:
            if exceptions[code_1st] == '0':  # Check if the direction is '0'
                continue  # Skip this row
            elif exceptions[code_1st]:
                displayed_directions.append((row_number, exceptions[code_1st], code_1st))
        elif not direction_2nd and direction_7th == 'laikina':
            # If 2nd column is empty and 7th column is 'laikina', show 'laikina'
            displayed_directions.append((row_number, 'laikina', code_1st))  # Add code_1st
        elif direction_2nd:
            # If the direction exists (not empty), show the direction as is
            displayed_directions.append((row_number, direction, code_1st))  # Add code_1st
        # Exclude entries where direction is empty and no exception is provided
        elif not direction_2nd:
            displayed_directions.append((row_number, 'kitos kryptys', code_1st))

    # If there are no valid directions to display, return None
    if not displayed_directions:
        error()
        return None

    # Create a list of directions to check for duplicates
    directions_list = [d[1] for d in displayed_directions]

    if len(directions_list)==1:
        stop_code = code_1st
        return stop_code

    street_names = []

    for idx, (row_number, direction, code_1st) in enumerate(displayed_directions, start=1):
        if directions_list.count(direction) > 1:
            direction_8th = direction_8th_column[row_number]  # Get the street name from the 8th column
            street_names.append((direction, direction_8th))
            displayed_directions[idx - 1] = (row_number, direction, code_1st)

    # Check for duplicate directions and append street name if needed
    for idx, (row_number, direction, code_1st) in enumerate(displayed_directions, start=1):
        try:
            direction_8th = direction_8th_column[row_number]  # Get the street name from the 8th column
        except:
            direction_8th = '?'
        
        # Check for duplicate directions and append street name if needed
        if directions_list.count(direction) > 1:
            # Append street name if the direction is duplicated
            if street_names.count((direction,direction_8th)) == 1:
                direction += f" ({direction_8th})"
            else:
                direction += f" ({code_1st})"
            
            displayed_directions[idx - 1] = (row_number, direction, code_1st)

    # Sort the directions alphabetically by direction text
    displayed_directions.sort(key=lambda x: x[1].lower())  # Sort by direction, case-insensitive

    # Print directions
    print()
    print(stop_name)
    print("Kryptis:")
    for idx, (row_number, direction, code_1st) in enumerate(displayed_directions, start=1):
        print(f"  {idx}: {direction}")

    # Ask user to select a direction
    while True:
        try:
            user_choice = input("Nr.: ")  # Get user's choice
            user_choice = int(user_choice)
            if 1 <= user_choice <= len(displayed_directions):
                selected_row_number = displayed_directions[user_choice - 1][0]  # Get the row number for selected direction
                stop_code = rows[selected_row_number - 1][0]  # Get stop code from the first column
                return stop_code
            else:
                error()  # Invalid choice, prompt again
        except:
            bug_report=list(user_choice)
            try:
                bug_report[0]=int(bug_report[0])
                if len(bug_report)==2 and bug_report[1]=='/' and 1 <= bug_report[0] <= len(displayed_directions):
                    selected_row_number = displayed_directions[bug_report[0] - 1][0]  # Get the row number for selected direction
                    stop_code_bug = rows[selected_row_number - 1][0]  # Get stop code from the first column
                    
                    with open(bugs_file, mode='a', encoding='utf-8') as file12:
                        file12.writelines(f"{stop_code_bug}\n")
                    print('Dėkojame už informaciją.')
                else:
                    error()
            except TypeError:
                error()
            except ValueError:
                if not user_choice:
                    print()
                    return None
                else:
                    error()
            except IndexError:
                if not user_choice:
                    print()
                    return None
                else:
                    error()

def get_departures(stop_code):
    url = "https://www.stops.lt/vilnius/departures2.php?stopid=" + stop_code
    response = requests.get(url)
    response.encoding = 'utf-8'

    with open(departures_file, 'w', encoding='utf-8') as file10:
        file10.write(response.text)

    with open(departures_file, 'r', encoding='utf-8') as file11:
        if len(file11.readlines())<=3:
            empty=True
        else:
            empty=False

        return empty

def process_departures():
    route_types = []
    route_numbers = []
    route_variants = []
    departure_times = []
    vehicle_attributes = []
    fleet_numbers = []
    trip_directions = []

    with open(departures_file, mode='r', encoding='utf-8') as file4:
        file4_csv_reader = csv.reader(file4, delimiter=',')
        rows = list(file4_csv_reader)

        # Skip the first row as it contains the stop name
        for row in rows[1:]:
            if len(row) < 6:
                continue

            route_type = row[0].strip().lower()
            route_number = row[1].strip().upper()
            trip_variant = row[2].strip()
            departure_time_unix = row[3].strip()
            vehicle_block = row[4].strip()
            trip_direction = row[5].strip()

            # Append route type
            route_types.append(route_type)

            # Process and append route number
            if route_type == 'trol':
                route_number = f"T{route_number}"
            if route_number == '&NBSP;':
                route_number = '86'
            
            if any(char.isdigit() for char in trip_variant):
                route_variant = '*'
            else:
                route_variant = ' '
            
            route_variants.append(route_variant)
            route_numbers.append(route_number)

            # Convert and append departure time
            with open(os_file, 'r') as os_data_2:
                content = os_data_2.read()
                if content == '2':
                    departure_time = datetime.fromtimestamp(int(departure_time_unix)-3*60*60).strftime('%H:%M:%S')
                elif content == '3':
                    departure_time = datetime.fromtimestamp(int(departure_time_unix)).strftime('%H:%M:%S')
                else:
                    departure_time = datetime.fromtimestamp(int(departure_time_unix)-2*60*60).strftime('%H:%M:%S')

            departure_times.append(departure_time)

            # Separate and append vehicle attributes and fleet number
            vehicle_attributes.append(''.join(filter(str.isalpha, vehicle_block)))
            fleet_numbers.append(''.join(filter(str.isdigit, vehicle_block)))

            # Append trip direction

            trip_direction = trip_direction.replace('&ndash;','-')

            with open(os_file, 'r') as os_data_7:
                if os_data_7.read() == '3':
                    trip_direction = trip_direction.replace('autobusų parkas','AP')
                    trip_direction = trip_direction.replace('Autobusų parkas','AP')
                    trip_direction = trip_direction.replace('troleibusų parkas','TP')
                    trip_direction = trip_direction.replace('Troleibusų parkas','TP')
                    trip_direction = trip_direction[:6]

            trip_directions.append(trip_direction)

    # Return all prepared lists
    return route_types, route_numbers, route_variants, departure_times, vehicle_attributes, fleet_numbers, trip_directions

def process_realtime_data(fleet_numbers):
    # Prepare lists to store extracted data
    vehicle_delays = []
    trip_ids = []
    schedule_numbers = []

    # Open the GPS file and process its data
    with open(gps_file, mode='r', encoding='utf-8') as file7:
        file7_csv_reader = csv.reader(file7, delimiter=',')
        rows = list(file7_csv_reader)

        # Iterate through fleet numbers to find matches
        for fleet_number in fleet_numbers:
            for row in rows:
                if len(row) < 15:  # Ensure row has at least 15 columns
                    continue

                if row[3].strip() == fleet_number:  # Match fleet number in the 4th column

                    # Extract, convert, and append vehicle_delay from the 10th column
                    try:
                        negative_delay = False
                        delay_seconds = int(row[9].strip())
                        if delay_seconds<0:
                            negative_delay = True
                        
                        delay_minutes = abs(delay_seconds) // 60
                        delay_seconds = abs(delay_seconds) % 60
                        formatted_delay = f"{'-' if negative_delay == True else ' '}{abs(delay_minutes):02}:{delay_seconds:02}"
                        vehicle_delays.append(formatted_delay)
                    except:
                        vehicle_delays.append("00:00")  # Default if conversion fails

                    # Extract and append schedule_number from the 15th column
                    trip_id = row[14]
                    schedule_parts = trip_id.strip().split('-')
                    try:
                        schedule_number = schedule_parts[1].zfill(2)
                    except:
                        schedule_number = '? '

                    trip_ids.append(trip_id)
                    schedule_numbers.append(schedule_number)

    # Return the collected lists
    return vehicle_delays, trip_ids, schedule_numbers

def assign_vehicle_model(vehicle_numbers):
    models = []
    sizes = []

    with open(os_file, 'r') as os_data_6:
        if os_data_6.read() == '3':
            models_file = models_file_2
        else:
            models_file = models_file_1
   
    with open(models_file, mode='r', encoding='utf-8') as file8:
        file8_csv_reader = csv.DictReader(file8)
        rows = list(file8_csv_reader)
            
    with open(regional_models_file, 'r') as file16:
        file16_csv_reader = csv.reader(file16, delimiter=';')
        regional_rows = list(file16_csv_reader)
    
    if vehicle_numbers[0].isdecimal():

        for fleet_number in vehicle_numbers:
            matched_model = None
            matched_size = None

            if int(fleet_number) <= 54:
                for regional_row in regional_rows:
                    if fleet_number == regional_row[0]:
                        matched_model = regional_row[2]
                        matched_size = regional_row[3]
                        break

            else:
                for i, row in enumerate(rows):
                    start_value = int(row['Start'])
                    next_start_value = int(rows[i + 1]['Start']) if i + 1 < len(rows) else float('inf')

                    if start_value <= int(fleet_number) < next_start_value:
                        matched_model = row['Model']
                        matched_size = row['Size']
                        break

            models.append(matched_model if matched_model else "Neįvestas modelis")
            sizes.append(matched_size if matched_size else "?")
    
    else:
        for license_plate in vehicle_numbers:
            matched_model = None
            matched_size = None

            for regional_row in regional_rows:
                if license_plate == regional_row[1]:
                    matched_model = regional_row[2]
                    matched_size = regional_row[3]
                    break
        
        models.append(matched_model if matched_model else "Neįvestas modelis")
        sizes.append(matched_size if matched_size else "?")

    return models, sizes

def assign_schedule_type(route_numbers, trip_ids):
    schedule_types = []
    schedule_type_lengths = []

    with open(schedule_file, 'r', encoding='utf-8') as file22:
        file22_csv_reader = csv.reader(file22, delimiter=';')
        rows = list(file22_csv_reader)

    for route_number, trip_id_combined in zip(route_numbers, trip_ids):
        if not trip_id_combined:
            schedule_type_lengths.append(0)
            schedule_types.append('')
            continue

        trip_id = trip_id_combined.split('-')

        raw_schedule_type = None
        raw_note = None
        schedule_type = None

        for row in rows:
            if trip_id[0] == row[0] and trip_id[1].replace('0','') == row[2] and trip_id[2] == row[1]:
                raw_schedule_type = row[3]
                raw_note = row[4]
                break
        
        if raw_schedule_type == '0':
            schedule_type = 'pt'
        elif raw_schedule_type == '1':
            schedule_type = '1p'
        else:
            schedule_type = '2p'
        
        with open(os_file, 'r', encoding='utf-8') as os_data_7:
            if os_data_7.read() != '3':
                if raw_note == '1':
                    schedule_type += '/1TP'
                elif raw_note == '2':
                    schedule_type += '/2TP'

                if route_number.replace('*', '') != trip_id[0].replace('A', '') and trip_id[0]:
                    schedule_type += f"/{trip_id[0].replace('A', '')}"
        
        schedule_type_lengths.append(len(schedule_type))
        schedule_types.append(schedule_type)
        
    return schedule_types, max(schedule_type_lengths)

def display_departures(name, departure_times, vehicle_delays, route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers, sizes, models, schedule_types, schedule_type_length):
    item = 1
    direction_length = 6
    model_length = 0
    number_length = 3

    for trip_direction in trip_directions:
        if len(trip_direction) > direction_length:
            direction_length = len(trip_direction)
    for model in models:
        if len(model) > model_length:
            model_length = len(model)
    for number in route_numbers:
        if len(number) > number_length:
            number_length = len(number)

    print(f"Stotelė: {name} | Laikas: {current_time()}")

    with open(os_file, 'r', encoding='utf-8') as os_data_7:
        if os_data_7.read() == '3':
            print(f'Išvyksta Nuokr. {"Nr.":>{number_length}} {"Graf.":<{schedule_type_length + 3}} {"Krpt.":^{direction_length - 2}} Dyd. Gar. Modelis')

            for departure_time, vehicle_delay, route_number, route_variant, trip_direction, schedule_number, fleet_number, size, model, schedule_type in zip(departure_times, vehicle_delays, route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers, sizes, models, schedule_types):
                print(f'{departure_time:<8} {vehicle_delay:<6} {route_number:>{number_length}}{route_variant}({schedule_type:<{schedule_type_length}}) {trip_direction:<{direction_length}} {size:>2} {fleet_number:>4} {model:<{model_length}}')

        else:
            if direction_length > 8:
                print(f'Išvyksta Nuokr. {"Nr.":>{number_length}} {"Graf.":<{schedule_type_length + 6}} {"Kryptis":^{direction_length - 1}}Dyd. Gar. {"Modelis":^{model_length-2}}')
            else:
                print(f'Išvyksta Nuokr. {"Nr.":>{number_length}} {"Graf.":<{schedule_type_length + 6}} {"Krpt.":^{direction_length - 2}} Dyd. Gar. {"Modelis":^{model_length-2}}')

            for departure_time, vehicle_delay, route_number, route_variant, trip_direction, schedule_number, fleet_number, size, model, schedule_type in zip(departure_times, vehicle_delays, route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers, sizes, models, schedule_types):
                print(f'{departure_time:<8} {vehicle_delay:<6} {route_number:>{number_length}}{route_variant}({schedule_number:<2}{"|" if schedule_type else ""}{schedule_type:<{schedule_type_length}}) {trip_direction:<{direction_length}} {size:>2} {fleet_number:>4} {model:<{model_length}}')

        item += 1

# Extra features

def enter_code():
    while True:
        try:
            code = input('Įveskite kodą: ')
            if not code:
                break
            return code
        except AttributeError:
            error()

def update_data():
    rip_txt("https://www.stops.lt/vilnius/vilnius/stops.txt", stops_file)
    rip_from_zipfile("http://stops.lt/vilnius/ridango/gtfs.zip")
    with open(date_file, 'w') as date:
        date.write(datetime.today().strftime('%Y.%m.%d'))
    print('Atnaujinti maršrutų ir stotelių duomenys.')
    print()

def view_trips(challenge):
    print()

    try:
        with open(challenge_file, 'r', encoding='utf-8') as file9:
            file9_csv_reader = csv.reader(file9, delimiter=';')
            rows = list(file9_csv_reader)

            base_rows = sorted(
                [row[:3] for row in rows],  # Keep only the first 3 elements of each row
                key=lambda row: (row[0].zfill(4), row[1], row[2])  # Sorting based on the first 3 elements
            )

            sorted_rows = []
            for base_row in base_rows:
                if base_row in sorted_rows:
                    sorted_rows[sorted_rows.index(base_row)][2] += ' (!)'
                else:
                    sorted_rows.append(base_row)

            rows = [row for row in rows if len(row) > 4]

    except FileNotFoundError:
        with open(challenge_file, 'w', encoding='utf-8') as file9:
            file9.write("") 
            rows = []
            sorted_rows = []

    if challenge:
        print(f"  Gar. D. Modelis")
        for row in sorted_rows:
            try:
                print(f"{row[0]:>6} {row[1]:<2} {row[2]}")
            except:
                pass
    else:
        model_length = 0
        direction_length = 0
        for row in rows:
            if len(row[2]) > model_length:
                model_length = len(row[2])
            if len(row[4]) > direction_length:
                direction_length = len(row[4])
        
        print(f"Nr. Marš.{'Kryptis':^{direction_length + 2}}Gar. D.{'Modelis':^{model_length}}")
        for item in range(len(rows)):
            number = str(item + 1)
            number += '.'
            try:
                print(f"{number:^4}{rows[item][3]:>4} {rows[item][4]:<{direction_length}} {rows[item][0]:>6} {rows[item][1]:<2} {rows[item][2]:<}")
            except:
                pass
    
    print()

def add_whole():
    print()

    added_size = None
    added_model = None

    whole_selection = input('Įveskite ilgį/modelį: ')
    if len(whole_selection) <= 2:
        whole_selection = whole_selection.lower()

        if whole_selection == ('t' or 'i'):
            print('  1. Autobusai')
            print('  2. Troleibusai')

            while True:
                mode_selection = input('Nr.: ')
                if mode_selection == '1':            
                    added_size = whole_selection
                    added_model = "(autobusai)"
                    break
                elif mode_selection == '2':
                    added_size = whole_selection
                    added_model = "(troleibusai)"
                    break
                else:
                    error()
        
        else:
            added_size = whole_selection
            added_model = ""

    else:
        added_size = ""
        added_model = whole_selection

    if added_size or added_model:
        with open(challenge_file, 'a+', encoding='utf-8', newline='') as file15:
            file15_csv_writer = csv.writer(file15, delimiter=';')
            file15_csv_writer.writerows([['Visi:', added_size, added_model]])

    print()

def add_vehicle_number(vehicle_number):

    model, size = assign_vehicle_model([vehicle_number])
    model = model[0]
    size = size[0]

    route = input('Nurodykite maršrutą: ')
    direction = input('Nurodykite kryptį: ')

    added_vehicle = [vehicle_number, size, model, route, direction]

    with open(challenge_file, 'a+', encoding='utf-8', newline='') as file17:
        file17_csv_writer = csv.writer(file17, delimiter=';')
        file17_csv_writer.writerows([added_vehicle])

def remove_trip():
    print()

    try:
        with open(challenge_file, 'r+', encoding='utf-8', newline='') as file18:
            file18_csv_reader = csv.reader(file18, delimiter=';')
            rows = list(file18_csv_reader)

    except FileNotFoundError:
        return

    while True:
        removal_selection = input('Ištrinamo įrašo nr.: ')

        if removal_selection == "":
            break

        elif removal_selection.isdecimal():
            try:
                rows.pop(int(removal_selection) - 1)
                break
            except IndexError:
                error()

        else:
            error()
    
    with open(challenge_file, 'w', encoding='utf-8', newline='') as file19:
        file19_csv_writer = csv.writer(file19, delimiter=';')
        file19_csv_writer.writerows(rows)
    print()

def tracking_selection():
    print()
    
    while True:
        viewing_decision = input('Pasirinkite/pridėkite: ')
        viewing_decision = viewing_decision.replace(" ","").upper()

        if viewing_decision == ".":
            view_trips(False)
        elif viewing_decision == ",":
            view_trips(True)
        elif viewing_decision == "+":
            add_whole()
        elif viewing_decision == "-":
            remove_trip()
        elif viewing_decision.isdecimal() or len(viewing_decision) == 6:
            add_vehicle_number(viewing_decision)
        elif viewing_decision == "":
            break
        else:
            error()
    
    print()

def analyze_route():

    while True:
        rip_txt("https://www.stops.lt/vilnius/gps_full.txt", gps_file)

        fleet_numbers = []
        models = []
        model_lengths = []
        sizes = []
        trip_starts = []
        trip_ids = []
        trip_directions = []
        direction_lengths = []
        schedule_numbers = []
    
        print()
        route_number = input('Nurodykite maršruto numerį: ')
        route_number = route_number.upper()
        route_numbers = []
        number = route_number

        if not route_number:
            print()
            break
        print()

        if 'T' in route_number:
            route_number = route_number.replace('T','')
            route_type = 'Troleibusai'
        else:
            route_type = 'Autobusai'
        
        with open(gps_file, mode='r', encoding='utf-8') as file5:
            csv_reader_file5 = csv.reader(file5, delimiter=',')
            rows = list(csv_reader_file5)

            for row in rows:
                if len(row) < 15:
                    continue

                if row[0] == route_type and row[1].upper() == route_number:
                    fleet_number = row[3]

                    trip_start = row[8]
                    try:
                        hours = (int(trip_start) // 60) % 24
                        minutes = int(trip_start) % 60
                        trip_start = f"{hours:02}:{minutes:02}"
                    except:
                        pass

                    trip_type = row[12]
                    trip_direction = row[13]
                    if re.search(r'\d+', trip_type):
                        trip_direction += '*'

                    trip_id = row[14]
                    schedule_parts = trip_id.strip().split('-')
                    try:
                        schedule_number = schedule_parts[1].zfill(2)
                    except:
                        schedule_number = '? '
                    
                    fleet_numbers.append(fleet_number)
                    trip_starts.append(trip_start)
                    trip_ids.append(trip_id)
                    trip_directions.append(trip_direction)
                    direction_lengths.append(len(trip_direction))
                    schedule_numbers.append(schedule_number)
        
        if not fleet_numbers:
            error()
        else:

            for fleet_number in fleet_numbers:
                model, size = assign_vehicle_model([fleet_number])
                models.append(model[0])
                model_lengths.append(len(model[0]))
                sizes.append(size[0])

            for i in range(len(trip_ids)):
                route_numbers.append(number)
            
            schedule_types, schedule_type_length = assign_schedule_type(route_numbers, trip_ids)
            schedule_type_length = max(schedule_type_length, 1)

            zipped_data = zip(fleet_numbers, models, sizes, trip_starts, trip_directions, schedule_numbers, schedule_types)
            sorted_data = sorted(zipped_data, key=lambda x: int(x[5]) if x[5].isdigit() else float('inf'))

            model_length = max(model_lengths)
            direction_length = max(direction_lengths)

            print(f"Maršrutas: {number} | TP kiekis: {len(fleet_numbers)} | Laikas: {current_time()}")
            print(f'{"Graf.":<{schedule_type_length + 4}} Dyd. Nr. {"Modelis":^{model_length}}  {"Kryptis":^{direction_length}} Išv.')

            for fleet_number, model, size, trip_start, trip_direction, schedule_number, schedule_type in sorted_data:
                print(f'{schedule_number:<2} {"(" if schedule_type else " "}{schedule_type:<{schedule_type_length}}{")" if schedule_type else " "} {size:>2} {fleet_number:>4} {model:<{model_length}}  {trip_direction:<{direction_length}} {trip_start}')

def search_vehicle():
    while True:
        rip_txt("https://www.stops.lt/vilnius/gps_full.txt", gps_file)

        route_number = None

        print()
        fleet_number = input('Nurodykite garažinį numerį: ')

        if not fleet_number:
            print()
            break
        print()

        with open(gps_file, mode='r', encoding='utf-8') as file5:
            csv_reader_file5 = csv.reader(file5, delimiter=',')
            rows = list(csv_reader_file5)

        for row in rows:
            if len(row) < 15:
                continue

            if row[3] == fleet_number:
                route_type = row[0]
                
                if route_type == 'Troleibusai':
                    route_number = 'T' + row[1]
                else:
                    route_number = row[1]
                
                trip_start = row[8]
                try:
                    hours = (int(trip_start) // 60) % 24
                    minutes = int(trip_start) % 60
                    trip_start = f"{hours:02}:{minutes:02}"
                except:
                    pass

                trip_type = row[12]
                trip_direction = row[13]
                if re.search(r'\d+', trip_type):
                    route_number += '*'

                trip_id = row[14]
                schedule_parts = trip_id.strip().split('-')
                try:
                    schedule_number = schedule_parts[1].zfill(2)
                except:
                    schedule_number = '?'
                
                break
            
        if route_number:
            model, size = assign_vehicle_model([fleet_number])
            model = model[0]
            size = size[0]

            schedule_type, ext = assign_schedule_type([route_number], [trip_id])
            schedule_type = schedule_type[0]
            schedule_type = schedule_type.replace('2p', '2 pam.').replace('1p', '1 pam.').replace('pt', 'pertr.').replace('/', ', iš ')
        
            print(f"TP: {model}, nr. {fleet_number} ({size}) ")

            if trip_start:
                print(f'Maršrutas: {route_number} ({schedule_number}{": " if schedule_type else ""}{schedule_type}) {trip_direction} | Išvyksta: {trip_start}')
            else:
                print(f'Maršrutas: {route_number} ({schedule_number}{": " if schedule_type else ""}{schedule_type}) {trip_direction}')

        else:
            error()

def feedback():
    with open(bugs_file, 'a+') as feedback_file:
        print(feedback_file.read())
    print()

def add_favorite():
    print()

    print('Stotelių trumpiniai:')
    with open(favorites_file, 'r', encoding='utf-8') as file19:
        file19_csv_reader = csv.reader(file19, delimiter=';')
        rows = list(file19_csv_reader)
    
    for item in range(len(rows)):
        print(f'  {item + 1}. {rows[item][2]}')
    print()

    while True:
        selection = input('Redaguojamas nr.: ')
        
        try:
            if int(selection) <= len(rows):
                pass
            else:
                raise ValueError
        except:
            if selection == "":
                break
            else:
                error()
                continue
        
        while True:
            entered_stop = input('Pridėkite stotelę: ')
            if entered_stop == "":
                break
            
            else:
                try:
                    entered_stop = normalize(entered_stop)
                    partial_matches = match_entered_stop(entered_stop)
                except:
                    error()
                    continue

                if not partial_matches:
                    error()
                    continue

                stop_directions_rows, name = handle_partial_matches(partial_matches)

                if stop_directions_rows is None:
                    continue

                stop_code = determine_stop_direction(name, stop_directions_rows)
            
            if stop_code:
                rows[int(selection) - 1][1] = stop_code

                print()
                stop_name = input('Įveskite trumpinio pavadinimą: ')
                rows[int(selection) - 1][2] = stop_name

                print()
                break

            else:
                error()
        
    with open(favorites_file, 'w', encoding='utf-8', newline='') as file21:
        file21_csv_writer = csv.writer(file21, delimiter=';')
        file21_csv_writer.writerows(rows)

    print()

def get_favorite(selection):
    stop_code = None
    stop_name = None
    
    with open(favorites_file, 'r', encoding='utf-8') as file19:
        file19_csv_reader = csv.reader(file19, delimiter=';')
        rows = list(file19_csv_reader)
    
    for row in rows:
        if row[0] == selection:
            stop_code = row[1]
            stop_name = row[2]
            break

    return stop_code, stop_name

def display_instructions():
    print()

    print('STOTELĖS. Gaukite pasirinktos stotelės artimiausios valandos išvykimo laikus:')
    print('  Įveskite norimos stotelės pavadinimą arba jo fragmentą.')
    print('  Norėdami pasirinkti stotelę nurodydami jos kodą, įveskite „=“.')
    print('  Talpos/dydžio žymėjimas: mk – mikroautobusai | m – mažos talpos | t – standartinės talpos | ti – pailginti viengubi | i – dvigubi.')
    print('  Maršruto žymėjimas: T – troleibusų maršrutas | * – reisas alternatyvia trasa.')
    print('  Grafiko žymėjimas: 2p – 2 pam. | 1p – 1 pam. | pt – pertraukiamas | /00 – maršrutas, su kuriuo sujungtas grafikas | /1TP, /2TP – grafiką aptarnaujantis parkas.')
    print('  Galite toliau įvesti kitos stotelės pavadinimą arba atnaujinti prognozes įvedus tuščią eilutę.')
    print('  Krypčių pasirinkimų sąraše radę nelogiškų, nesuprantamų ar klaidinančių krypčių, užfiksuokite su / ženklu (jei klaidinga 1: „1/“ ir t.t.).')
    print()
    
    print('MARŠRUTO PERŽIŪRA. Gaukite informaciją apie šiuo metu pasirinktame maršrute kursuojančias transporto priemones:')
    print('  Norėdami pasiekti, įveskite „?“.')
    print('  Įveskite norimo peržiūrėti maršruto numerį. Troleibusų maršrutus pasiekite pradėdami numerį „t“ raide. Norėdami išeiti, įveskite tuščią eilutę.')
    print()

    print('TRANSPORTO PRIEMONĖS PAIEŠKA. Gaukite informaciją, kuriuo maršrutu kursuoja pasirinkta transporto priemonė:')
    print('  Norėdami pasiekti, įveskite „!“.')
    print('  Įveskite norimos surasti transporto priemonės garažinį numerį. Norėdami išeiti, įveskite tuščią eilutę.')
    print()
    
    print('SEKIMAS. Sekite transporto priemones, kuriomis jau esate važiavę:')
    print('  Norėdami pasiekti, įveskite „-“. Įvedę tuščią eilutę išeisite iš režimo. Toliau nurodytos režimo funkcijos, pasiekiamos tam tikrais klavišais.')
    print('  Peržiūra: „.“ – maršrutų ir transporto priemonių peržiūra | „,“ – surikiuota transporto priemonių peržiūra.')
    print('  Įvestis: garažinis (miesto ar VRAP)/valstybinis (kitų įmonių) numeris – įvedama transporto priemonė, nuvažiuotas maršrutas ir kryptis.')
    print('  Įvestis: „+“ – pridedamas visas modelis ar dydis/talpa')
    print()

    print('TRUMPINIAI. Pridėkite ir naudokitės trumpiniais, norėdami greitai pamatyti pasirinktų stotelių išvykimo laikus:')
    print('  Norėdami pasiekti trumpinių nustatymą, įveskite „*“. Įvedę tuščią eilutę išeisite iš režimo')
    print('  Trumpinius galite nustatyti įvedę numerį 1–9. Tada galėsite surasti stotelę bei priskirti trumpiniui pavadinimą.')
    print('  Paprastame režime įvedę skaičius 1–9 pasieksite savo trumpinius.')
    print()

    print('ATSILIEPIMAI. Pamatykite savo praneštą klaidingą informaciją (stotelių kodus).')
    print('  Norėdami pasiekti, įveskite „/“. Išeisite automatiškai.')
    print()

    print('ATNAUJINIMAS. Naujinkite programos duomenis:')
    print('  Maršrutų ir stotelių duomenys atnaujinti ',end='')
    with open(date_file, 'r') as date:
        print(date.read(),end='')
    print('.')
    print('  Norėdami atnaujinti, įveskite „+“.')
    print()

def enter_stop(stop_code):
    while True:
        entered_stop = input('Įveskite: ')
        
        if stop_code and not entered_stop:
            return None, stop_code, None
        
        elif entered_stop == "0":
            display_instructions()

        elif entered_stop == "=":
            print()
            stop_code = enter_code()
            if stop_code:
                return None, stop_code, stop_code
            else:
                print()

        elif entered_stop == "+":
            try:
                update_data()
            except requests.exceptions.ConnectionError:
                connection()

        elif entered_stop == "-":
            tracking_selection()

        elif entered_stop == "?":
            try:
                analyze_route()
            except requests.exceptions.ConnectionError:
                connection()
        elif entered_stop == "!":
            try:
                search_vehicle()
            except requests.exceptions.ConnectionError:
                connection()

        elif entered_stop == "/":
            feedback()

        elif entered_stop.isdigit():
            try:
                stop_code, stop_name = get_favorite(entered_stop)
            except requests.exceptions.ConnectionError:
                connection()

            if stop_code:
                return None, stop_code, stop_name
            else:
                error()

        elif entered_stop == "*":
            try:
                add_favorite()
            except requests.exceptions.ConnectionError:
                connection()

        else:
            return entered_stop, None, None

# Base functions

def os_check():
    with open(os_file, 'r+') as os_data:
        if not os_data.read():
            print('Pasirinkitę savo operacinę sistemą:')
            print('  1. Windows')
            print('  2. Android')
            print('  3. iOS')
            while True:
                os = input('Nr.: ')
                if os == '1' or os == '2' or os == '3':
                    break
                else:
                    error()
            os_data.truncate(0)
            os_data.write(os)
            print()

def display_information():
    with open(os_file, 'r') as os_data_5:
        if os_data_5.read() != '1':
            print('Naudodami programą laikykite mobilųjį įrenginį horizontaliai.')
            print()
    print('Programos instrukcijos pasiekiamos GitHub puslapyje arba įvedus skaitmenį „0“.')
    print()

def execute_program():
    stop_code = None

    while True:
        entered_stop, stop_code, code_as_name = enter_stop(stop_code)

        if not stop_code:
            try:
                entered_stop = normalize(entered_stop)
                partial_matches = match_entered_stop(entered_stop)
            except requests.exceptions.ConnectionError:
                connection()
                continue
            except:
                error()
                continue

            if not partial_matches:
                print('Nėra atitikmenų.')
                continue

            stop_directions_rows, name = handle_partial_matches(partial_matches)

            if stop_directions_rows is None:
                continue

            stop_code = determine_stop_direction(name, stop_directions_rows)

        if code_as_name:
            name = code_as_name

        if stop_code:
            print()

            while True:
                rip_txt("https://www.stops.lt/vilnius/gps_full.txt", gps_file)

                empty = get_departures(stop_code)
                if empty:
                    print('Laikų nėra.')
                    print()
                    break

                else:
                    route_types, route_numbers, route_variants, departure_times, vehicle_attributes, fleet_numbers, trip_directions = process_departures()
                    vehicle_delays, trip_ids, schedule_numbers = process_realtime_data(fleet_numbers)
                    models, sizes = assign_vehicle_model(fleet_numbers)
                    schedule_types, schedule_type_length = assign_schedule_type(route_numbers, trip_ids)

                    display_departures(
                        name, departure_times, vehicle_delays,
                        route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers,
                        sizes, models,
                        schedule_types, schedule_type_length
                    )

                print()
                break

# Main code

def main():
    print('STOPS v2.1_10 | https://github.com/Lanxtot/stops | © Lanxtot')   
    print()

    os_check()
    display_information()
    execute_program()

if __name__ == "__main__":
    main()
