from sqllex.classes import PostgreSQLx

di_ = dir(PostgreSQLx)

di_.sort()

for d in di_:
    print(d)