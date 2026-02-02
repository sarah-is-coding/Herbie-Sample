import sys
VALID_CONTACT_TYPES = {'email', 'call', 'coffee'}

def main():
    employee_company = {}  # employee_name -> company_name
    company_partner_counts = {}  # company_name -> {partner_name -> contact_count}

    if len(sys.argv) < 2:
        print("Usage: python company_relationships.py <input_file>")
        return 1

    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            command = parts[0]

            match command:
                case "Partner":
                    # not needed for output
                    pass

                case "Company":
                    company_name = parts[1]
                    company_partner_counts.setdefault(company_name, {})  # partner counts map

                case "Employee":
                    employee_name, company_name = parts[1], parts[2]
                    employee_company[employee_name] = company_name
                    company_partner_counts.setdefault(company_name, {})

                case "Contact":
                    employee_name, partner_name, contact_type = parts[1], parts[2], parts[3]

                    if contact_type not in VALID_CONTACT_TYPES:
                        raise ValueError(f"Invalid contact type: {contact_type}")

                    try:
                        company_name = employee_company[employee_name]
                    except KeyError:
                        raise ValueError(f"Contact references unknown employee: {employee_name}")

                    partner_counts = company_partner_counts[company_name] 
                    partner_counts[partner_name] = partner_counts.get(partner_name, 0) + 1

    for company_name in sorted(company_partner_counts):
        counts = company_partner_counts[company_name]

        if not counts:
            print(f"{company_name}: No current relationship")
            continue

        best_strength = max(counts.values())
        # tie break alphabetically
        best_partner = min( 
            partner
            for partner, strength in counts.items()
            if strength == best_strength
        )
        print(f"{company_name}: {best_partner} ({best_strength})")
            
    return 0


if __name__ == "__main__":
    raise SystemExit(main())