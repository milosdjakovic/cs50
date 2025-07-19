import sqlite3
import os


def create_db(db_path, schema_path):
    conn = sqlite3.connect(db_path)

    with open(schema_path, "r") as f:
        schema_script = f.read()

    conn.executescript(schema_script)
    conn.commit()
    print(f"Database created and initialized at {db_path}")

    return conn


def seed_db(conn, seed_path):
    if not os.path.exists(seed_path):
        return

    try:
        with open(seed_path, "r") as f:
            seed_script = f.read()

        conn.executescript(seed_script)
        conn.commit()
        print("Database seeded with initial data")
    except Exception as e:
        print(f"Error seeding database: {e}")


def init_db(db_name="main.db"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, db_name)
    schema_path = os.path.join(current_dir, "schema.sql")
    seed_path = os.path.join(current_dir, "seed.sql")

    if os.path.exists(db_path):
        print(f"Database already exists at {db_path}. No action taken.")
        return db_path

    conn = create_db(db_path, schema_path)
    seed_db(conn, seed_path)
    conn.close()

    return db_path


if __name__ == "__main__":
    init_db()
