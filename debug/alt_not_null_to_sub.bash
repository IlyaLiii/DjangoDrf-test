#!/bin/bash
psql -h 0.0.0.0 -p 5432 -U postgres -d base2 -c "ALTER TABLE books ALTER COLUMN subcategories DROP NOT NULL;"