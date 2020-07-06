BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "auth_group_permissions" VALUES (29,3,73);
INSERT INTO "auth_group_permissions" VALUES (30,3,75);
INSERT INTO "auth_group_permissions" VALUES (31,3,76);
INSERT INTO "auth_group_permissions" VALUES (32,1,74);
INSERT INTO "auth_group_permissions" VALUES (33,1,77);
INSERT INTO "auth_group_permissions" VALUES (34,3,78);
INSERT INTO "auth_group_permissions" VALUES (35,5,73);
INSERT INTO "auth_group_permissions" VALUES (36,5,75);
INSERT INTO "auth_group_permissions" VALUES (37,3,36);
INSERT INTO "auth_group_permissions" VALUES (38,3,79);
INSERT INTO "auth_group_permissions" VALUES (39,1,41);
INSERT INTO "auth_group_permissions" VALUES (40,1,42);
INSERT INTO "auth_group_permissions" VALUES (41,1,43);
INSERT INTO "auth_group_permissions" VALUES (42,1,44);
INSERT INTO "auth_group_permissions" VALUES (43,4,80);
INSERT INTO "auth_group_permissions" VALUES (44,8,106);
INSERT INTO "auth_group_permissions" VALUES (45,8,93);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
COMMIT;
