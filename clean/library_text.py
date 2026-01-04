from library_functions import (

    load_subjects, load_locations,
    search_subject, search_classmark, search_location
)
#   basically loads the fuctions from library_funtions.py to be used in this file
def main():

    subjects = load_subjects()
    locations = load_locations()

    while True :

        print("\n📖 Terminal Library Search System ")

        print("1. Search by Subject Name or part-name")

        print("2. Search by Classmark")
        print("3. Search by Location")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':

            term = input("Enter subject name or part of it: ").strip()
            if not term:
                print("Please enter a search term.")
                continue
            results = search_subject(term, subjects, locations)
            if results:
                print("\n Results:")
                for r in results:
                    print(" -", r)
            else:
                print("No matches found.")

        elif choice == '2':
            cm = input("Enter classmark (e.g., QA): ").strip()
            if not cm:
                print("Please enter a classmark.")
                continue
            results = search_classmark(cm, subjects, locations)
            if results:
                print("\n Results:")
                for r in results:
                    print(" -", r)
            else:
                print("No matches found.")

        elif choice == '3':
            print("Available locations (examples):")
            for loc in locations:
                print(" -", loc.get('Location', ''))
            loc_name = input("Enter the  location : ").strip()
            if not loc_name:
                print("Please enter a location name.")
                continue
            results = search_location(loc_name, subjects, locations)
            if results:
                print("\n Results:")
                for r in results:
                    print(" -", r)
            else:
                print("No matches found.")

        elif choice == '4':
            print(" Goodbye!  ")
            break
        else:
            print("Invalid choice. Enter 1,2,3 or 4.")

if __name__ == "__main__":
    main()
