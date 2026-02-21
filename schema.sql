-- Student table
create table Student (
  student_id bigint primary key,
  name varchar not null,
  email varchar not null unique,
  preferences text,
  study_level varchar,
  created_at timestamptz not null default now()
);

-- Task table
create table Task (
  task_id bigint primary key,
  title varchar not null,
  description varchar,
  deadline date not null,
  estimated_time bigint not null,
  status varchar not null, 
  created_at timestamptz not null default now(),
  student_id bigint not null,
  constraint task_student_id_fkey
    foreign key (student_id)
    references Student (student_id)
    on delete cascade
);

-- StudyPlan table
create table StudyPlan (
  plan_id bigint primary key,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  student_id bigint not null,
  constraint studyplan_student_id_fkey
    foreign key (student_id)
    references Student (student_id)
    on delete cascade
);
