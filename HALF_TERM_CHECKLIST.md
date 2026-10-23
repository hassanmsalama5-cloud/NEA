# One-week Half-Term Checklist

Use this checklist to track revision and practical tasks. For academic topics, tick an item only after reviewing the method/content, attempting exam-style questions, and marking/correcting your answers.

## Monday — Core foundations
- [ ] Maths: Arithmetic and geometric sequences
- [ ] Maths: Radians — arc length, sector area, area of a triangle
- [ ] Physics: Circular motion
- [ ] Physics: Simple Harmonic Motion (SHM)
- [ ] Computer Science: Databases
- [ ] Computer Science: Boolean algebra
- [ ] NEA: List unfinished development tasks and choose the first feature to complete

## Tuesday — Trigonometry and thermal physics
- [ ] Maths: Reciprocal trigonometric functions (cosec, sec, cot)
- [ ] Maths: Squared trigonometric identities
- [ ] Physics: Ideal gases
- [ ] Physics: Thermal physics
- [ ] Computer Science: Karnaugh maps
- [ ] Computer Science: Half adders and full adders
- [ ] UCAS: Work on the personal statement and identify remaining application tasks

## Wednesday — Mechanics and algorithms
- [ ] Maths: Double-angle formulae
- [ ] Maths: Harmonic form
- [ ] Physics: Kinematics and forces and motion
- [ ] Physics: Work, energy and power
- [ ] Computer Science: Data structures
- [ ] Computer Science: Depth-first search and breadth-first search
- [ ] NEA: Implement a feature and test it with suitable test data

## Thursday — Applications and programming
- [ ] Maths: Solving trigonometric equations
- [ ] Physics: Moments and equilibrium
- [ ] Physics: Materials and Hooke's law
- [ ] Computer Science: Algorithms
- [ ] Computer Science: Floating-point arithmetic
- [ ] Computer Science: Object-oriented programming
- [ ] NEA: Write development evidence that matches the updated code

## Friday — Consolidation and completion
- [ ] Maths: Timed mixed questions covering sequences/series, radians and trigonometry
- [ ] Physics: Density, pressure, liquid pressure, upthrust and Archimedes' principle
- [ ] Physics: Waves
- [ ] Computer Science: Compression, encryption and hashing
- [ ] Computer Science: Processor components and process/processor performance
- [ ] NEA: Review development section and update the write-up to match the code
- [ ] UCAS: Proofread the personal statement and complete remaining application tasks

## Saturday — Rest
- [ ] Take the day off from scheduled revision

## Sunday — Review and engineering courses
- [ ] Maths: Redo questions you got wrong earlier in the week
- [ ] Physics: Mixed exam questions on your weakest topics
- [ ] Computer Science: Timed mixed questions and review the error log
- [ ] Engineering course: Complete MATLAB Onramp
- [ ] Engineering course: Complete Simulink Onramp
- [ ] Engineering course: Complete Simscape Battery Onramp
- [ ] Final review: List anything unfinished to carry into the following week

## NEA — Code and documentation update checklist
Review the current implementation in GitHub before editing the write-up. These are checks to complete, not claims that the features are already working.

- [ ] Fix the seat-selection template loops so the inner loop iterates over each row's seats and the row label comes from the current row.
- [ ] Fix malformed seat button HTML attributes (for example, the missing equals sign in the class attribute).
- [ ] Make seat template property names consistent with the Python dictionaries (`id`, `row`, `number`, `booked`).
- [ ] Verify the selected-seat counter is wired to JavaScript; check that `static/seats.js` contains the required selection logic and is loaded by `seats.html`.
- [ ] Add or confirm CSS for the seat chart so seats display in rows and columns, with clear available, selected and unavailable states.
- [ ] Verify the Flask `select_seats` route passes the intended row data. Check the mismatch between `seat_by_row` and `row` variables.
- [ ] Test the full customer journey: sign in/sign up → choose genre → choose film → select screening → select seats.
- [ ] Confirm selected seats are validated against current availability and saved to the database; prevent two customers booking the same seat.
- [ ] Check validation and error messages for empty forms, invalid credentials, duplicate usernames, no films/screenings, no seats, and invalid requests.
- [ ] Verify database connections close on every code path and errors are handled safely.
- [ ] Test admin functions for adding, editing and deleting films/screenings if these are part of the intended design.
- [ ] Update the development write-up after testing each feature, including code extracts, test data, expected/actual results, fixes and screenshots.
- [ ] Align analysis, design, success criteria, testing and evaluation with features that are actually implemented.

## After every revision topic
- [ ] Recall key definitions, equations or methods without notes.
- [ ] Attempt exam-style questions.
- [ ] Mark answers and add mistakes to an error log.
- [ ] Reattempt missed questions later without looking at the solution.

## Notes
- Electricity and quantum physics were marked “to be confirmed” in the source revision document; check with the teacher whether to include them.
- The source lists “Simple” under Year 13 Physics; this is expanded to Simple Harmonic Motion as clarified.
- If a day is overloaded, move tasks forward rather than sacrificing question-marking or rest.