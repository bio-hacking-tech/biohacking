import pandas as pd
import numpy as np

# User-specific diet data
user = 0
diet = pd.read_excel('path/to/diet'+user+'.xlsx')
diet = diet.drop(['Unnamed: 0'], axis=1)

carbon = pd.read_excel('carbonfootprint_table.xlsx')

# Function to check food category and find alternatives
def check_category(food, carbon):
    category = None
    for j in range(len(carbon)):
        if carbon['food'][j] == food:
            category = carbon['category'][j]
            break
    _list = []
    for j in range(len(carbon)):
        if carbon['category'][j] == category:
            _list.append(carbon['food'][j])
    return _list

# Initialize variables and data structures for the algorithm
diet_week = diet
bh = diet_week.copy()
bh['Switch'] = np.nan
j = 0
dic = {}
indexes = []

switch = []
meal = []
new = []
calorie_reduction = []
impact_reduction = []
quantity = []

min_cal = 100
max_cal = 200

# Iterate through each unique date in the diet_week DataFrame
for k in diet_week.date.unique():
    print('\033[96mControl date:', k)
    dietmeal = diet_week[diet_week.date == k]
    for i in dietmeal.meal.unique():
        print('\033[94mControl meal: ', i)
        dietdata = dietmeal[dietmeal.meal == i]
        if not dietdata.empty:
            if dietdata.intake.sum() < 100:
                print('The meal has a low caloric intake (', str(dietdata.intake.sum()), '), so it does not need any change.')
            else:
                # Select the food with the highest caloric intake for replacement
                selection = dietdata[dietdata.category2 != 'Lipids and oils']
                selection = dietdata[dietdata.category2 != 'Salt']
                selection = dietdata[dietdata.category2 != 'Species']
                selection = dietdata[dietdata.category2 != 'Coffee and Tea']
                if selection.empty:
                    print('No foods to change')
                else:
                    change = selection.query('intake == intake.max()')
                    if len(change) > 1:
                        change = change.query('index == index.min()')
                    index = change.index[0]
                    print('Food to change:', change['food'], change['category2'])
                    print('Food to change:', change['food'], change['category'])
                    # Set thresholds
                    threshold_i = float(change['intake'])
                    threshold_m = float(change['quantity'])
                    threshold_c = float(change['carbon_footprint_impact'])
                    # Choose alternatives
                    df_meal = diet[diet.meal == i]
                    df_meal = df_meal[df_meal['date'].dt.weekday == change['date'][index].dayofweek]
                    df_alternative = df_meal[df_meal.food != change['food'].to_string(index=False)]
                    # Filter alternatives by category and criteria
                    df_alternative = df_alternative[df_alternative.category2 != 'Lipids and oils']
                    df_alternative = df_alternative[df_alternative.category2 != 'Salt']
                    df_alternative = df_alternative[df_alternative.category2 != 'Species']
                    df_alternative = df_alternative[df_alternative.category2 != 'Coffee and Tea']
                    df_alternative = df_alternative[df_alternative["category"].isin(check_category(change['category'][change.index[0]], carbon))]
                    df_alternative['intakeQ'] = df_alternative['intake'] * change['quantity'].values[0] / df_alternative['quantity']
                    df_alternative['carbon_impactQ'] = df_alternative['carbon_footprint_impact'] * change['quantity'].values[0] / df_alternative['quantity']

                    # If the carbon footprint threshold is NaN (not a number), select candidates based on intake only
                    if str(threshold_c) == 'nan':
                        candidate = df_alternative[(df_alternative['intakeQ'] < threshold_i) & (df_alternative['intakeQ'] > threshold_i * 0.2)]
                    else:
                        # Otherwise, select candidates based on both intake and carbon footprint
                        candidate = df_alternative[(df_alternative['intakeQ'] < threshold_i) & (df_alternative['intakeQ'] > threshold_i * 0.1) & (df_alternative['carbon_impactQ'] <= threshold_c)]

                    # If there are suitable candidates
                    if not candidate.empty:
                        indexes.append(index)
                        # Select the candidate with the minimum intake
                        candidate = candidate.query('intake == intake.min()')
                        # Drop unnecessary columns
                        candidate = candidate.drop(['intakeQ', 'carbon_impactQ'], axis=1)
                        ignores = ['Unnamed: 0', 'db', 'meal', 'date', 'quantity', 'food', 'category3', 'category2', 'category']
                        for column in candidate.columns:
                            if column not in ignores:
                                # Adjust the candidate's nutritional values based on the quantity to match the food to be replaced
                                candidate[column].values[0] = candidate[column].values[0] * change['quantity'].values[0] / candidate['quantity'].values[0]
                        # Update the quantity to match the food to be replaced
                        candidate['quantity'].values[0] = change['quantity'].values[0]

                        worst = change['food'].to_string(index=False)
                        q_worst = change['quantity'].values[0]
                        good = candidate['food'].to_string(index=False)
                        q_good = candidate['quantity'].values[0]

                        # Print the details of the replacement
                        print('\033[92m'+str(q_worst)+ ' g of '+worst+' are been switched with ' +str(q_good)+ ' g of '+good+'\n')
                        print('\033[92m'+str(change['intake'].values[0])+ ' kcal of '+worst+' are been switched with ' +str(candidate['intake'].values[0])+ ' kcal of '+good+'\n')
                        print('\033[92m'+str(change['carbon_footprint_impact'].values[0])+ ' kgeCo2 of '+worst+' are been switched with ' +str(candidate['carbon_footprint_impact'].values[0])+ ' kgeCo2 of '+good+'\n')
                        print('\033[92m'+change['category'].to_string(index=False)+ ' of '+worst+' is been switched with ' +candidate['category'].to_string(index=False)+ ' of '+good+'\n')

                        # Set the date and switch flag for the candidate
                        candidate['date'] = k
                        candidate['Switch'] = True

                        # Update the DataFrame with the new candidate
                        bh.loc[index] = candidate.iloc[0]
                        candidate.reset_index(drop=True, inplace=True)
                        change.reset_index(drop=True, inplace=True)

                        # Update the dictionary with the change
                        dic[tuple(candidate.loc[0])] = tuple(change.loc[0])

                        # Increment the switch counter
                        j += 1

                        # Append details of the change to the lists
                        quantity.append(candidate['quantity'].values[0])
                        switch.append(change['food'].to_string(index=False))
                        new.append(candidate['food'].to_string(index=False))
                        meal.append(change['meal'].to_string(index=False))
                        calorie_reduction.append(candidate['intake'].values[0] - change['intake'].values[0])
                        impact_reduction.append(candidate['carbon_footprint_impact'].values[0] - change['carbon_footprint_impact'].values[0])

                        # Print the number of changes made so far
                        print(len(quantity))
                    else:
                        # If no suitable candidates with both intake and carbon footprint criteria
                        if str(threshold_c) == 'nan':
                            candidate = df_alternative[(df_alternative['intakeQ'] < threshold_i)]
                        else:
                            candidate = df_alternative[(df_alternative['intakeQ'] < threshold_i) & (df_alternative['carbon_impactQ'] <= threshold_c)]
                        if not candidate.empty:
                            indexes.append(index)
                            candidate = candidate.query('intake == intake.min()')
                            candidate = candidate.drop(['intakeQ', 'carbon_impactQ'], axis=1)
                            ignores = ['Unnamed: 0', 'db', 'meal', 'date', 'quantity', 'food', 'category3', 'category2', 'category']
                            for column in candidate.columns:
                                if column not in ignores:
                                    candidate[column].values[0] = candidate[column].values[0] * change['quantity'].values[0] / candidate['quantity'].values[0]
                            candidate['quantity'].values[0] = change['quantity'].values[0]
                            worst = change['food'].to_string(index=False)
                            q_worst = change['quantity'].values[0]
                            good = candidate['food'].to_string(index=False)
                            q_good = candidate['quantity'].values[0]
                            print('\033[92m'+str(q_worst)+ ' g of '+worst+' are been switched with ' +str(q_good)+ ' g of '+good+'\n')
                            print('\033[92m'+str(change['intake'].values[0])+ ' kcal of '+worst+' are been switched with ' +str(candidate['intake'].values[0])+ ' kcal of '+good+'\n')
                            print('\033[92m'+str(change['carbon_footprint_impact'].values[0])+ ' kgeCo2 of '+worst+' are been switched with ' +str(candidate['carbon_footprint_impact'].values[0])+ ' kgeCo2 of '+good+'\n')
                            print('\033[92m'+change['category'].to_string(index=False)+ ' of '+worst+' is been switched with ' +candidate['category'].to_string(index=False)+ ' of '+good+'\n')
                            candidate['date'] = k
                            candidate['Switch'] = True
                            bh.loc[index] = candidate.iloc[0]
                            candidate.reset_index(drop=True, inplace=True)
                            change.reset_index(drop=True, inplace=True)
                            dic[tuple(candidate.loc[0])] = tuple(change.loc[0])
                            j += 1
                            quantity.append(candidate['quantity'].values[0])
                            switch.append(change['food'].to_string(index=False))
                            new.append(candidate['food'].to_string(index=False))
                            meal.append(change['meal'].to_string(index=False))
                            calorie_reduction.append(candidate['intake'].values[0] - change['intake'].values[0])
                            impact_reduction.append(candidate['carbon_footprint_impact'].values[0] - change['carbon_footprint_impact'].values[0])
                            print(len(quantity))
                        else:
                            # If no candidates at all
                            print('\033[93mNo candidate')
                            for b in df_alternative.index:
                                print('Intake ', df_alternative['intakeQ'][b])
                                print('Carb imp ', df_alternative['carbon_impactQ'][b])
                            continue
        else:
            print('\033[93mNo data')
            continue

# Create a summary DataFrame for dietary changes
dictionary_diet = pd.DataFrame({'Food to change': switch, 'Alternative food': new, 'Quantity': quantity, 'Meal': meal,
                                'Calories reduction [kcal]': calorie_reduction, 'Carbon footprint impact reduction [kgeCo2]': impact_reduction})
print()
if bh.equals(diet):
    print("\033[91mNo changes")
else:
    print("\033[92mDone ", j, " changes")
