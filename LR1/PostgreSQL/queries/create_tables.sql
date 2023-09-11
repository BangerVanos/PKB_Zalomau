CREATE TABLE vendors (
  id VARCHAR (3) PRIMARY KEY,
  name varchar(50),
  status SMALLSERIAL,
  city varchar(50)
);

CREATE TABLE details (
	id VARCHAR (3) PRIMARY KEY,
	name VARCHAR (50),
	color VARCHAR (50),
	size VARCHAR (3),
	city VARCHAR (50)
);

CREATE TABLE projects (
	id VARCHAR (4) PRIMARY KEY,
	name VARCHAR (50),
	city VARCHAR (50)
);

CREATE TABLE details_for_projects (
	vendor_id VARCHAR (3),
	detail_id VARCHAR (3),
	project_id VARCHAR (4),
	amount SMALLINT,
	FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE SET NULL,
	FOREIGN KEY (detail_id) REFERENCES details (id) ON DELETE SET NULL,
	FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
);
