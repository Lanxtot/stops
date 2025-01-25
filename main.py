# Imports

import re
import requests
import csv
import os
from datetime import datetime, timedelta
from zipfile import ZipFile

# Files

stops_file = 'stops_list.csv'
departures_file = 'departures.csv'
gps_file = 'gps_data.csv'
models_file = 'models.csv'
challenge_file = 'challenge.csv'
ridango_stops_file = 'stops.csv'
schedule_file = 'schedule_types.csv'
bugs_file = 'bugs.txt'
date_file = 'date.txt'
os_file = 'os.txt'

# Mini functions

def error():
    print('Prašome patikslinti.')

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

def get_gtfs_data(url,selected_file):
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

def get_and_extract_zip(gtfs_file):
    """
    Downloads a GTFS zip file from the given URL, extracts 'stops.txt' and 'stop_times.txt',
    and renames them to 'stops.csv' and 'stop_times.csv'.

    Parameters:
        gtfs_file (str): URL of the GTFS zip file.

    Returns:
        None
    """
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
    get_gtfs_data("https://www.stops.lt/vilnius/vilnius/stops.txt", stops_file)

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
    if len(unique_values) >= 10 or len(unique_values) == 0:
        error()
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
        except ValueError:
            error()
            if not selection:
                return None, None
        except IndexError:
            error()
            if not selection:
                return None, None

def determine_stop_direction(stop_name, stop_directions_rows):
    # Read the exceptions.csv file and create a dictionary with Code and Option
    exceptions_file = 'exceptions.csv'
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
        except KeyError:
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
        except ValueError:
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
                error()
                if not user_choice:
                    print()
                    return None
            except IndexError:
                error()
                if not user_choice:
                    print()
                    return None

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

def analyze_departures():
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
            trip_directions.append(trip_direction)

    # Return all prepared lists
    return route_types, route_numbers, route_variants, departure_times, vehicle_attributes, fleet_numbers, trip_directions

def analyze_gps_data(fleet_numbers):
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
                    except ValueError:
                        vehicle_delays.append("00:00")  # Default if conversion fails

                    # Extract and append schedule_number from the 15th column
                    trip_id = row[14]
                    schedule_parts = trip_id.strip().split('-')
                    try:
                        schedule_number = schedule_parts[1].zfill(2)
                    except IndexError:
                        schedule_number = ' ?'

                    trip_ids.append(trip_id)
                    schedule_numbers.append(schedule_number)

    # Return the collected lists
    return vehicle_delays, trip_ids, schedule_numbers

def determine_vehicle_model(fleet_numbers):
    models = []
    sizes = []

    # Read the models_file and store its contents in a list for comparison
    with open(models_file, mode='r', encoding='utf-8') as file8:
        file8_csv_reader = csv.DictReader(file8)
        rows = list(file8_csv_reader)  # Store all rows in a list

    # Iterate over each fleet_number
    for fleet_number in fleet_numbers:
        matched_model = None
        matched_size = None

        # Iterate over rows in the models file
        for i, row in enumerate(rows):
            start_value = int(row['Start'])
            next_start_value = int(rows[i + 1]['Start']) if i + 1 < len(rows) else float('inf')

            if start_value <= int(fleet_number) < next_start_value:
                matched_model = row['Model']
                matched_size = row['Size']
                break

        # Append the matched model and size to the respective lists
        models.append(matched_model if matched_model else "Neįvestas modelis")
        sizes.append(matched_size if matched_size else "?")

    return models, sizes

def display_departures(name, departure_times, vehicle_delays, route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers, sizes, models):
    item = 1
    direction_length = 0
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
    if direction_length > 7:
        print(f'Išvyksta Nuokr. {"Nr.":>{number_length}} Graf. {"Kryptis":^{direction_length}}Dyd. Gar. {"Modelis":^{model_length-2}}')
    else:
        print(f'Išvyksta Nuokr. {"Nr.":>{number_length}} Graf. {"Krpt.":^{direction_length-1}} Dyd. Gar. {"Modelis":^{model_length-2}}')

    for departure_time, vehicle_delay, route_number, route_variant, trip_direction, schedule_number, fleet_number, size, model in zip(departure_times, vehicle_delays, route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers, sizes, models):
        print(f'{departure_time:<8} {vehicle_delay:<6} {route_number:>{number_length}}{route_variant}({schedule_number:<2}) {trip_direction:<{direction_length}}  {size:>2} {fleet_number:>4} {model:<{model_length}}')

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
    get_and_extract_zip("http://stops.lt/vilnius/ridango/gtfs.zip")
    with open(date_file, 'w') as date:
        date.write(datetime.today().strftime('%Y.%m.%d'))
    print('Atnaujinti maršrutų ir stotelių duomenys.')
    print()

def challenge():
    print()

    try:
        with open(challenge_file, 'r', encoding='utf-8') as file9:
            file9_csv_reader = csv.reader(file9, delimiter=',')
            rows = list(file9_csv_reader)

            sorted_rows = sorted(rows, key=lambda row: (row[0].zfill(4), row[1], row[2]))

    except FileNotFoundError:
        with open(challenge_file, 'w', encoding='utf-8') as file9:
            file9.write("") 
            rows = []

            sorted_rows = sorted(rows, key=lambda row: (row[0].zfill(4), row[1], row[2]))
    
    with open(challenge_file, 'w', encoding='utf-8', newline='') as file9:
        file9_csv_writer = csv.writer(file9, delimiter=',')
        file9_csv_writer.writerows(sorted_rows)

    # Print the sorted rows
    for row in sorted_rows:
        try:
            print(f'{row[0]:>4} {row[1]:<2} {row[2]}')
        except IndexError:
            pass

    print()

    while True:
        challenge_decision = input('Pridėkite: ')
        
        if not challenge_decision:
            print()
            return
        
        try:
            # Fleet number handling
            fleet_number = int(challenge_decision)
            if fleet_number < 555 or fleet_number > 8050:
                error()
                continue
            
            existing_row = next((row for row in rows if row and str(row[0]).isdigit() and int(row[0]) == fleet_number), None)
            
            if existing_row:
                rows.remove(existing_row)
                print('Ištrinta.')
            else:
                model, size = determine_vehicle_model([fleet_number])
                rows.append([fleet_number, *size, *model])
            
        except ValueError:
            if challenge_decision == '+':
                inp = input('Įveskite ilgį/modelį: ')

                selection_type = None

                if inp=='t' or inp=='i':
                    print('  1. Autobusai')
                    print('  2. Troleibusai')
                    while True:
                        selection_type = input('Nr.: ')
                        if selection_type == '1':
                            selection_type = 'Autobusai'
                            break
                        elif selection_type == '2' and inp =='i':
                            inp = ''
                            selection_type = 'Škoda 15Tr'
                            break
                        elif selection_type == '2' and inp =='t':
                            selection_type = 'Troleibusai'
                            break
                        else:
                            error()

                if len(inp)<3:
                    rows.append(['Visi', inp, selection_type])
                else:
                    rows.append(['Visi', '', inp])
            else:
                error()
        
        # Write updated rows back to the file
        with open(challenge_file, 'w', newline='', encoding='utf-8') as file15:
            file15_csv_writer = csv.writer(file15, delimiter=',')
            file15_csv_writer.writerows(rows)

def display_gps_data():

    while True:
        get_gtfs_data("https://www.stops.lt/vilnius/gps_full.txt", gps_file)

        fleet_numbers = []
        models = []
        model_lengths = []
        sizes = []
        trip_starts = []
        trip_directions = []
        direction_lengths = []
        schedule_numbers = []
    
        print()
        route_number = input('Nurodykite maršruto numerį: ')
        route_number = route_number.upper()
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
                    except ValueError:
                        pass

                    trip_type = row[12]
                    trip_direction = row[13]
                    if re.search(r'\d+', trip_type):
                        trip_direction += '*'

                    trip_id = row[14]
                    schedule_parts = trip_id.strip().split('-')
                    try:
                        schedule_number = schedule_parts[1].zfill(2)
                    except IndexError:
                        schedule_number = ' ?'
                    
                    fleet_numbers.append(fleet_number)
                    trip_starts.append(trip_start)
                    trip_directions.append(trip_direction)
                    direction_lengths.append(len(trip_direction))
                    schedule_numbers.append(schedule_number)
        
        if not fleet_numbers:
            error()
        else:

            for fleet_number in fleet_numbers:
                model, size = determine_vehicle_model([fleet_number])
                models.append(model[0])
                model_lengths.append(len(model[0]))
                sizes.append(size[0])

            zipped_data = zip(fleet_numbers, models, sizes, trip_starts, trip_directions, schedule_numbers)
            sorted_data = sorted(zipped_data, key=lambda x: int(x[5]) if x[5].isdigit() else float('inf'))

            model_length = max(model_lengths)
            direction_length = max(direction_lengths)

            print(f"Maršrutas: {number} | TP kiekis: {len(fleet_numbers)} | Laikas: {current_time()}")
            print(f'Gr. D. Nr. {"Modelis":^{model_length}}  {"Kryptis":^{direction_length}} Išv.')

            for fleet_number, model, size, trip_start, trip_direction, schedule_number in sorted_data:
                print(f'{schedule_number:<3}{size:>2} {fleet_number:>4} {model:<{model_length}}  {trip_direction:<{direction_length}} {trip_start}')

def search_gps_data():
    while True:
        get_gtfs_data("https://www.stops.lt/vilnius/gps_full.txt", gps_file)

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
                    except ValueError:
                        pass

                    trip_type = row[12]
                    trip_direction = row[13]
                    if re.search(r'\d+', trip_type):
                        route_number += '*'

                    trip_id = row[14]
                    schedule_parts = trip_id.strip().split('-')
                    try:
                        schedule_number = schedule_parts[1].zfill(2)
                    except IndexError:
                        schedule_number = '?'
                    
                    break
            
        if route_number:
            model, size = determine_vehicle_model([fleet_number])
            model = model[0]
            size = size[0]
        
            print(f"TP: {model}, nr. {fleet_number} ({size}) ")

            if trip_start:
                print(f'Maršrutas: {route_number} ({schedule_number}) {trip_direction} | Išvyksta: {trip_start}')
            else:
                print(f'Maršrutas: {route_number} ({schedule_number}) {trip_direction}')

        else:
            error()

def feedback():
    with open(bugs_file, 'a+') as feedback_file:
        print(feedback_file.read())
    print()

def enter_stop(stop_code):
    while True:
        entered_stop = input('Įveskite: ')
        
        if stop_code and not entered_stop:
            return None, stop_code, None
        elif entered_stop == "=":
            print()
            stop_code = enter_code()
            if stop_code:
                return None, stop_code, stop_code
            else:
                print()
        elif entered_stop == "+":
            update_data()
        elif entered_stop == "-":
            challenge()
        elif entered_stop == "?":
            display_gps_data()
        elif entered_stop == "!":
            search_gps_data()
        elif entered_stop == "/":
            feedback()
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

    print('STOTELĖS. Gaukite pasirinktos stotelės artimiausios valandos išvykimo laikus:')
    print('  Įveskite norimos stotelės pavadinimą arba jo fragmentą.')
    print('  Norėdami pasirinkti stotelę nurodydami jos kodą, įveskite „=“. Norėdami išeiti iš šio režimo, įveskite tuščią eilutę.')
    print('  Talpos/dydžio žymėjimas: mk – mikroautobusai | m – mažos talpos | t – standartinės talpos | ti – pailginti viengubi | i – dvigubi.')
    print('  Maršruto žymėjimas: T – troleibusų maršrutas | * – reisas alternatyvia trasa.')
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
    print('  Norėdami pasiekti, įveskite „-“.')
    print('  Įvestis: skaičius – užfiksuojamas pasinaudotas garažinis numeris | „+“ – pridedamas visas modelis ar dydis | tuščia eilutė – išeiti iš režimo.')
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

def execute_program():
    stop_code = None

    while True:
        entered_stop, stop_code, code_as_name = enter_stop(stop_code)

        if not stop_code:
            try:
                entered_stop = normalize(entered_stop)
                partial_matches = match_entered_stop(entered_stop)
            except AttributeError:
                error()
                continue

            if not partial_matches:
                error()
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
                get_gtfs_data("https://www.stops.lt/vilnius/gps_full.txt", gps_file)

                empty = get_departures(stop_code)
                if empty:
                    print('Laikų nėra.')
                    print()
                    break

                else:
                    route_types, route_numbers, route_variants, departure_times, vehicle_attributes, fleet_numbers, trip_directions = analyze_departures()
                    vehicle_delays, trip_ids, schedule_numbers = analyze_gps_data(fleet_numbers)
                    models, sizes = determine_vehicle_model(fleet_numbers)
                    display_departures(
                        name, departure_times, vehicle_delays,
                        route_numbers, route_variants, trip_directions, schedule_numbers, fleet_numbers,
                        sizes, models
                    )

                print()
                break

# Main code

def main():
    print('STOPS v2.1 TESTING BUILD 06 | https://github.com/Lanxtot/stops | © Lanxtot')   
    print()

    os_check()
    display_information()
    execute_program()

if __name__ == "__main__":
    main()