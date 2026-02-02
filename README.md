# Herbie-Sample

## How to Run and Test

```bash
python parse_relationships.py <relationships file>
```

Testing is done by running the program against different input files and verifying the output. In addition to the example from the prompt, I included small input files to cover tie breaking behavior and invalid contact references.

## How I Approached the Problem

I started by focusing on the question driving the output:
For each company, which Drive partner has the most total contacts with that company's employees?

From there, the main challenge was connecting pieces of information given in the input. It became clear that contacts would drive the computation of relationship strength. When we read in a contact command, we are given the employee and partner for that contact. As long as we can resolve an employee to a company, we can track partner contact counts by company. This thinking led me to create these two mappings:

employee_company: employee -> company  
company_partner_counts: company -> partner contact counts

This keeps the data close to the problem statement and makes the relationship strength easy to compute and reason about. In a real system, I would expect employees, partners, and companies to be represented as separate entities with direct relationships between them, which would allow the same data to answer a wider range of questions.

I first built a version that tracked the primary partner while parsing contacts as a single pass approach, which made the output straightforward. When I later added tie breaking logic, the update logic started to feel too complex, so I used ChatGPT to sanity check the approach. This pushed me toward computing the primary partner at output time instead, which simplified the logic and avoided repeated incremental computation.

The problem description does not specify how to handle ties when multiple partners have the same contact strength with a company. For my solution, I chose a simple alphabetical tie break. In a real system, a more meaningful approach might be to break ties by prioritizing interpersonal contacts (e.g., coffee > call > email), since those signals may better reflect the strength of a relationship. I intentionally did not implement that here to avoid inventing business rules.

## Assumptions and Edge Cases

The prompt specifies that the input is well formed, so the code assumes:

- Employees always reference an existing company
- Employee names are globally unique
- Partner names, employee names, and company names are all single words
- There are no incorrectly formatted lines such as missing arguments or invalid command structures

Edge cases:

- Blank lines are skipped
- Duplicated names handled with `setdefault`
- Contacts that reference an employee who hasn't been declared trigger a `ValueError`
- Tie breaks (alphabetical fallback)

## Use of LLM Tools

I implemented an initial working solution independently, with light Copilot usage for basic syntax and iteration. I then used ChatGPT as a design review and refactoring aid to sanity check tradeoffs, simplify logic, and improve readability. In particular, it helped me reconsider when derived values (such as the primary partner) should be computed. I also used it to help polish the README.
All final code was reviewed, understood, and edited by me, and I'm comfortable explaining any part of it.
