CREATE TABLE IF NOT EXISTS mechanics (
  id TEXT PRIMARY KEY,
  description TEXT NOT NULL,
  cost INTEGER NOT NULL CHECK (cost >= 0),
  evidence TEXT NOT NULL
);

INSERT INTO mechanics (id, description, cost, evidence)
VALUES ('demo.roll', 'Spend stamina to roll', 20,
        'Five accepted; sixth refused')
ON CONFLICT(id) DO UPDATE SET
  description=excluded.description,
  cost=excluded.cost,
  evidence=excluded.evidence;

SELECT id, cost, evidence FROM mechanics;
