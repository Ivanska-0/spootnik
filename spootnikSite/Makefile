USER = alumnodb
DDBB = sputnik
DUMP = db/dump.sql

TARGET = -U $(USER) $(DDBB)

reset_db:
	dropdb $(TARGET)
	createdb $(TARGET)
	cat $(DUMP) | psql $(TARGET)

test_db: reset_db
	@cat db/test_populate.sql | psql $(TARGET)
