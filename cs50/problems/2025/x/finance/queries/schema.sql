CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE holdings (
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    current_shares INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, symbol),
    FOREIGN KEY (user_id) REFERENCES users (id)
  );
CREATE INDEX idx_symbol ON holdings (symbol);
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL, -- Positive for buy, negative for sell
    price REAL NOT NULL,
    datetime DATETIME DEFAULT (STRFTIME ('%Y-%m-%d %H:%M:%f', 'NOW')),
    FOREIGN KEY (user_id) REFERENCES users (id)
  );
CREATE INDEX idx_transactions_user_symbol ON transactions (user_id, symbol);
CREATE INDEX idx_transactions_datetime ON transactions (datetime);
