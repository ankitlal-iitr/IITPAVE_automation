import os
import subprocess
import re
import csv

E3, E4 = 240.2, 76.8
h2, h3 = 100, 450
poisson_ratio = 0.35
tyre_pressure = 0.56
wheel_load = 20000

E1_list = [2000, 2500, 3000, 3500, 4000]
E2_list = [300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
h1_list = [40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0]

base = r"C:\Users\Rajeshwar Lal\Desktop\IITPAVE\IRC_37_IITPAVE\IRC_37_IITPAVE\IRC_37_IITPAVE"
exe = os.path.join(base, "IITPAVE.exe")
inp = os.path.join(base, "IITPAVE.IN")
out = os.path.join(base, "IITPAVE.OUT")
csv_path = os.path.join(base, "automated_iitpave_response.csv")

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "E1", "E2", "E1/E2", "h1",
        "sigz_h1", "sigt_h1", "sigr_h1", "tau_h1", "epz_h1", "ept_h1", "epr_h1", "h1/2",
        "sigz_h1/2", "sigt_h1/2", "sigr_h1/2", "tau_h1/2", "epz_h1/2", "ept_h1/2", "epr_h1/2"
    ])

    for E2 in E2_list:
        for E1 in E1_list:
            for h1 in h1_list:
                with open(inp, "w") as f:
                    f.write("4\n")
                    f.write(f"{E1} {E2} {E3} {E4}\n")
                    f.write(f"{poisson_ratio} {poisson_ratio} {poisson_ratio} {poisson_ratio}\n")
                    f.write(f"{h1} {h2} {h3}\n")
                    f.write(f"{wheel_load} {tyre_pressure}\n")
                    f.write("2\n")
                    f.write(f"{h1} 0\n{h1/2} 0\n")
                    f.write("2\n")

                subprocess.run([exe], cwd=base, check=True)

                values = {"h1": {}, "h1/2": {}}
                with open(out, "r") as f:
                    for line in f:
                        tokens = line.strip().split()
                        if not tokens or 'L' in tokens[0]:
                            continue
                        nums = re.findall(r'[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?', line)
                        if len(nums) >= 10:
                            z, r = float(nums[0]), float(nums[1])
                            if r != 0:
                                continue
                            data = dict(zip(
                                ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"],
                                [nums[i] for i in [2, 3, 4, 5, 7, 8, 9]]
                            ))
                            if abs(z - h1) < 0.5 and not values["h1"]:
                                values["h1"] = data
                            elif abs(z - h1 / 2) < 0.5 and not values["h1/2"]:
                                values["h1/2"] = data

                if values["h1"] and values["h1/2"]:
                    writer.writerow([
                        E1, E2, round(E1 / E2, 2), h1,
                        *[values["h1"].get(k, "") for k in ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"]],
                        h1 / 2,
                        *[values["h1/2"].get(k, "") for k in ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"]]
                    ])
