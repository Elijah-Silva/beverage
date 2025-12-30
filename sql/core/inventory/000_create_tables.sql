SET SEARCH_PATH = core;

CREATE TABLE batch_inventory
(
	batch_inventory_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	product_id         INT         NOT NULL,
	order_item_id      INT,
	production_date    DATE,
	quantity_count     INT CHECK (quantity_count >= 0),
	quantity_weight    NUMERIC(7, 2) CHECK (quantity_weight >= 0),
	is_in_stock        BOOLEAN     NOT NULL CHECK (is_in_stock IN ('TRUE', 'FALSE')),
	received_date      DATE        NOT NULL DEFAULT CURRENT_DATE,
	created_date       DATE         NOT NULL DEFAULT NOW(),
	last_modified_date DATE         NOT NULL DEFAULT NOW(),
	batch_code			TEXT		NOT NULL,
	FOREIGN KEY (product_id) REFERENCES core.products (product_id),
	FOREIGN KEY (order_item_id) REFERENCES core.order_items (order_item_id),
	UNIQUE (product_id, order_item_id),
	CONSTRAINT check_quantity CHECK ((quantity_count IS NULL) != (quantity_weight IS NULL))
);


CREATE TABLE session_batch_inventory (
    session_batch_inventory_id  INT     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id                  INT     NOT NULL,
    batch_inventory_id          INT     NOT NULL,
	production_date             DATE,
    quantity_used               NUMERIC(7,2)     NOT NULL CHECK (quantity_used >= 1),
    batch_code                  TEXT,
    unit                        TEXT    NOT NULL CHECK (unit IN ('pcs', 'g')),
	UNIQUE (session_id, batch_inventory_id)
);