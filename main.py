from app.database import check_db_connection


def main():
    print("Hello from smoothie-registration!")
    check_db_connection()


if __name__ == "__main__":
    main()
    
