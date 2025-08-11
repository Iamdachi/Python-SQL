-- We join students to rooms on room_id, Index on students.room_id speeds up the JOIN.
CREATE INDEX idx_students_room_id ON students(room_id);

--  Index on students.birthday for calculating age in aggregate functions.
CREATE INDEX idx_students_birthday ON students(birthday);

-- Index on students.sex for filtering/grouping by sex in the last query:
CREATE INDEX idx_students_sex ON students(sex);

--Composite index on (room_id, sex) speeds up grouping by room and filtering distinct sexes:
CREATE INDEX idx_students_roomid_sex ON students(room_id, sex);
