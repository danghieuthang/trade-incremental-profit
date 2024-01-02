from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import math

# the dictionary key is the day start, the value is the stake value
STAKES = {
    1: 100,
    3: 290,
    10: 460,
    12: 440,
}

# The rate that daily earning
RATE_DAILY = 0.8/100

# Total date expired of one stake
STAKE_EXPIRED = 250

# Minimum value for new stake
MINIMUM_STAKE_VALUE = 100

# The start day of the trade, map with first key of stakes
START_DATE =  datetime(2023, 12, 19)

# End date for add profit to stake
END_DATE =datetime(2024, 4, 30)

# get total stake value at specific day
def caculate_total_stake(stakes, day_earning):
    total = 0
    for day_stake in stakes:
        if(day_earning >= day_stake):
            total +=stakes[day_stake]
        if((day_earning-day_stake) > STAKE_EXPIRED):
            total -= stakes[day_stake]
    return total

def calculate_profit(value, rate, days):
    # calculate profit with compound interest
    return value * (rate * days)

def calculate_profit_with_compound_interest(stake, rate, days):
    # calculate profit with compound interest
    return stake * (1 + rate) ** days

def calculate_profit_with_compound_interest_with_new_stake(stake, rate, days, new_stake):
    return stake * (1 + rate) ** days + new_stake

def currency(x, pos):
    'The two args are the value and tick position'
    return '${:1.0f}'.format(x*1e-6)


incremental_datasets = []
total_stake_value = 0
total_profit = 0
incremental_time = (END_DATE - START_DATE).days
stakes = STAKES

for day in range(1, incremental_time):
    total_stake_value = caculate_total_stake(stakes, day)
    profit_in_one_day = calculate_profit(total_stake_value, RATE_DAILY, 1)
    total_profit += profit_in_one_day
    if(total_profit>=MINIMUM_STAKE_VALUE):
        stakes[day] = total_profit
        total_profit = 0
        dataset = {
                'date': START_DATE+timedelta(days=day),
                'stake': total_stake_value,
                'days': day,
                'minimum_day_for_next_stake': math.ceil(MINIMUM_STAKE_VALUE/profit_in_one_day),
                'profit': profit_in_one_day,
            }
        incremental_datasets.append(dataset)

end_incremental_time = START_DATE+timedelta(days=day)


earning_datasets = []
day_earning = incremental_time+1
start_earning_time = START_DATE+timedelta(days=day_earning)
total_profit = 0

while True:
    total_stake_value = caculate_total_stake(stakes, day_earning)
    profit_in_one_day = calculate_profit(total_stake_value, RATE_DAILY, 1)
    total_profit += profit_in_one_day
    dataset = {
        'date': START_DATE+timedelta(days=day_earning),
        'stake': total_stake_value,
        'days': day_earning,
        'profit': total_profit,
    }
    earning_datasets.append(dataset)
    day_earning += 1
    if(total_stake_value<=0):
        break
    
end_earning_time = START_DATE+timedelta(days=day_earning)



import pandas as pd

incremental_df = pd.DataFrame(incremental_datasets, columns=['date', 'stake', 'days', 'minimum_day_for_next_stake', 'profit'])
earning_df = pd.DataFrame(earning_datasets, columns=['date', 'stake', 'days', 'profit'])
