drop table IF EXISTS consumers;
drop table IF EXISTS professionals;

create TABLE consumers (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

insert into consumers (id, username, password) values (1, "Joe", "pass1");
insert into consumers (id, username, password) values (2, "Kate", "pass2");

create TABLE professionals (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fullname TEXT NOT NULL,
  qualifications TEXT NOT NULL,
--  psychologist, psychiatrist, social worker, therapist
  profession TEXT NOT NULL,
--  for example: Depression, Anxiety, Bipolar, PTSD, OCD, Personality Disorders, Eating Disorders & Body Image Issues etc.
  specialties TEXT NOT NULL,
  languages TEXT NOT NULL,
  details TEXT NOT NULL
);

-- profiles scrapped and mixed from https://www.psychologytoday.com/us?tr=Hdr_Brand
insert into professionals (id, username, password, fullname, qualifications, profession, specialties, languages, details)
values
(1, "doc1", "pass", "Jonh Smith", "PsyD", "psychologist", "Depression, Personality Disorders", "english, german",
    "I offer practical solutions for overcoming feelings of hopelessness and lack of meaning.
    My practice is based on an empathetic, non-judgmental, and motivational style.
    I will help you to learn and incorporate coping skills to deal with issues you are facing in life.
    My treatment is solution-focused, and I delve deep into my clients' day to day lives,
    helping them identify problem areas.
    I then combat these with practical tools like the DBT-informed skills and mindfulness practices."),
(2, "doc2", "pass", "Kate Connor", "MD", "psychiatrist", "Eating Disorders & Body Image Issues", "english",
    "My expertise includes the management of Major Depression, Eating Disorders, Panic Disorder and Anxiety with or
    without the addition of medication, depending on the patient's preference. I have extensive experience in working
    with patients in various stages of preparation for bariatric surgery and their unique postoperative medication needs."),
(3, "doc3", "pass", "Ana Clarc", "MSN,  PMHNP,  BC", "Psychiatric Nurse Practitioner", "Anxiety, Trauma and PTSD", "english, italian",
    "My goal is to help you get your life back. If you can not function the way yo'd like to because of anxiety,
    depression, trauma, or, during this pandemic, isolation, loneness, despair, I can help you figure out realistic
    strategies to help you get your life back. It's hard work but worth it. Everyone needs a hand up once in awhile."),
(4, "doc4", "pass", "Alan Black", "MD,  ABIHM, IFMCP", "Psychiatrist", "Child or Adolescent, Trauma and PTSD", "english, spanish",
    "I am happy to work with patients who are reluctant to take medications and it appears that pharmacologic treatment
    could be of some benefit but is not absolutely necessary. I apply the precision medicine principles: using individualized,
    patient-centered and science based approach to diagnose and treat my patients. I combine the benefits of modern science with
    the focus on lifestyle, environmental and genetic factors.I empower my patients to be partners in the healing process."),
(5, "doc5", "pass", "Joan Martinez", "MD", "Psychiatrist", "Addiction, Alcohol Use", "spanish, english",
    "I treat a variety of psychiatric conditions including (but not limited to) psychiatric emergencies and urgent consults for depression,
    anxiety, psychosis, panic attacks, drug detox, and Medication Assisted Treatment for drug and alcohol abuse. I see patient 6 yrs old
    and up. I am dual trained in Family Medicine and Psychiatry and this gives me confidence to treat psychiatric
    conditions and weed out any medical conditions that can present with psychiatric complaints.
    I work in a multi disciplinary practice with different clinicians and treat a broad spectrum of psychiatric conditions.");

-- full test search extension FTS5
drop table IF EXISTS profile_search;
create VIRTUAL TABLE profile_search using fts5(id, fullname, qualifications, profession, profile);
insert into  profile_search SELECT id, fullname, qualifications, profession, fullname || ' ' || qualifications || ' ' || profession || ' ' || specialties || ' ' || languages || ' ' || details as profile FROM professionals;