from extract import main as extract_main
from transform import main as transform_main
from load import main as load_main


def main():
    print("=" * 60)
    print("CHILE ECONOMIC DATA PIPELINE")
    print("=" * 60)

    try:
        print("\n[1/3] EXTRACT")
        extract_main()

        print("\n[2/3] TRANSFORM")
        transform_main()

        print("\n[3/3] LOAD")
        load_main()

    except Exception as error:
        print("\nPIPELINE FAILED")
        print(f"Error: {error}")
        raise

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()