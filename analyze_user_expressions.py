# Manual analysis of user's expressions

def analyze_expressions():
    """Analyze which test cases are needed for full coverage"""
    
    print("EXPRESSION ANALYSIS:")
    print("Expression 1: (A or B) and C")
    print("Expression 2: A and B") 
    print("Expression 3: A and not C")
    print()
    
    print("TRUTH TABLE ANALYSIS:")
    print("A  B  C | Exp1 | Exp2 | Exp3 | Branches Hit")
    print("--------|------|------|------|-------------")
    
    test_cases = []
    for A in [False, True]:
        for B in [False, True]:
            for C in [False, True]:
                # Calculate expression results
                exp1 = (A or B) and C
                exp2 = A and B
                exp3 = A and not C
                
                # Determine which branches are hit
                branches = []
                branches.append("exp1_true" if exp1 else "exp1_false")
                branches.append("exp2_true" if exp2 else "exp2_false") 
                branches.append("exp3_true" if exp3 else "exp3_false")
                
                test_cases.append({
                    'A': A, 'B': B, 'C': C,
                    'exp1': exp1, 'exp2': exp2, 'exp3': exp3,
                    'branches': branches
                })
                
                print(f"{str(A)[0]}  {str(B)[0]}  {str(C)[0]} | {str(exp1)[0]:4s} | {str(exp2)[0]:4s} | {str(exp3)[0]:4s} | {', '.join(branches)}")
    
    print()
    print("BRANCH COVERAGE ANALYSIS:")
    all_branches = set()
    for tc in test_cases:
        all_branches.update(tc['branches'])
    
    print(f"Total branches to cover: {sorted(all_branches)}")
    
    print()
    print("MINIMUM TEST CASES NEEDED:")
    
    # Find minimum test cases needed
    branches_needed = {"exp1_true", "exp1_false", "exp2_true", "exp2_false", "exp3_true", "exp3_false"}
    
    print("To hit all branches, we need:")
    print("- exp1_true:  Need (A or B) and C = True  -> A=T,B=F,C=T or A=F,B=T,C=T or A=T,B=T,C=T")
    print("- exp1_false: Need (A or B) and C = False -> A=F,B=F,C=any or any,any,C=F")  
    print("- exp2_true:  Need A and B = True         -> A=T,B=T,C=any")
    print("- exp2_false: Need A and B = False        -> A=F,any,any or any,B=F,any")
    print("- exp3_true:  Need A and not C = True     -> A=T,any,C=F") 
    print("- exp3_false: Need A and not C = False    -> A=F,any,any or any,any,C=T")
    
    print()
    print("STRATEGIC TEST CASES:")
    strategic_cases = [
        {"A": True, "B": True, "C": True, "hits": ["exp1_true", "exp2_true", "exp3_false"]},
        {"A": True, "B": False, "C": False, "hits": ["exp1_false", "exp2_false", "exp3_true"]},
        {"A": False, "B": False, "C": False, "hits": ["exp1_false", "exp2_false", "exp3_false"]},
    ]
    
    for i, case in enumerate(strategic_cases, 1):
        A, B, C = case["A"], case["B"], case["C"]
        exp1 = (A or B) and C
        exp2 = A and B
        exp3 = A and not C
        
        print(f"Test {i}: A={A}, B={B}, C={C}")
        print(f"  exp1={(A or B) and C} -> {'exp1_true' if exp1 else 'exp1_false'}")
        print(f"  exp2={A and B} -> {'exp2_true' if exp2 else 'exp2_false'}")
        print(f"  exp3={A and not C} -> {'exp3_true' if exp3 else 'exp3_false'}")
        print()
    
    covered_branches = set()
    for case in strategic_cases:
        A, B, C = case["A"], case["B"], case["C"]
        exp1 = (A or B) and C
        exp2 = A and B
        exp3 = A and not C
        covered_branches.add("exp1_true" if exp1 else "exp1_false")
        covered_branches.add("exp2_true" if exp2 else "exp2_false") 
        covered_branches.add("exp3_true" if exp3 else "exp3_false")
    
    print(f"Strategic cases cover: {sorted(covered_branches)}")
    print(f"All branches covered: {covered_branches == branches_needed}")
    print(f"Reduction: {len(strategic_cases)}/8 = {len(strategic_cases)/8*100:.1f}% of original")

if __name__ == "__main__":
    analyze_expressions()