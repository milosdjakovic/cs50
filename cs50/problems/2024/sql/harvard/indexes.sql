CREATE INDEX "idx_enrollments_student_id" ON "enrollments" ("student_id");

CREATE INDEX "idx_enrollments_course_id" ON "enrollments" ("course_id");

CREATE INDEX "idx_satisfies_course_id" ON "satisfies" ("course_id");

CREATE INDEX "idx_courses_department_number_semester" ON "courses" ("department", "number", "semester");

CREATE INDEX "idx_courses_semester" ON "courses" ("semester");

CREATE INDEX "idx_courses_title_semester" ON "courses" ("title", "semester");
