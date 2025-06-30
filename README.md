# IITPAVE_automation


---

## How It Works

1. Loops through combinations of:
   - Bituminous layer modulus (E1)
   - DBM layer modulus (E2)
   - Bituminous layer thickness (h1)

2. Writes each combination into an `IITPAVE.IN` file.

3. Runs `IITPAVE.exe` via command line.

4. Parses `IITPAVE.OUT` file:
   - Extracts stress/strain values at depth = h1 and h1/2
   - Ignores values with `'L'` suffix (as per IRC:37-2018)

5. Appends valid results to a CSV file.

---

## Assumptions Based on IRC:37-2018

- **Wheel Load:** 20000 N  
- **Tyre Pressure:** 0.56 MPa  
- **Poisson’s Ratio:** 0.35 for all layers  

---

## Output Variables (CSV)

Each row includes:

- E1, E2, h1, E1/E2
- For both depths (h1 and h1/2):  
  - `sigz`, `sigt`, `sigr`, `tau`, `epz`, `ept`, `epr`

Sample output file: `automated_iitpave_response.csv`

---

## Report and Screenshots

A detailed PDF report includes:

- Methodology   
- Code explanation with snippets  
- Output sample and manual validation  
- Conclusion
