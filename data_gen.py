import pandas as pd
import numpy as np
import random

# Setting seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_data(n_samples=705):
    platforms = ['Instagram', 'YouTube', 'Snapchat', 'Threads', 'LinkedIn', 'WhatsApp', 'Twitter']
    countries = ['USA', 'India', 'UK', 'Canada', 'Australia', 'Germany', 'Brazil', 'Nigeria', 'Japan', 'Other']
    academic_levels = ['High School', 'Undergraduate', 'Graduate']
    relationship_statuses = ['Single', 'In Relationship', 'Complicated']
    
    data = []
    for _ in range(n_samples):
        age = random.randint(16, 25)
        gender = random.choice(['Male', 'Female'])
        academic_level = random.choice(academic_levels)
        country = random.choice(countries)
        usage_hours = round(random.uniform(1.5, 8.5), 2)
        platform = random.choice(platforms)
        
        # Logic for addiction score (BSMAS)
        # BSMAS ranges from 6 to 30. We'll simulate 6 items then sum them.
        bsmas_items = [random.randint(1, 5) for _ in range(6)]
        # Add correlation with usage hours
        if usage_hours > 6:
            bsmas_items = [min(5, x + random.randint(1, 2)) for x in bsmas_items]
        
        addicted_score = sum(bsmas_items)
        
        # Impact indicators
        affects_academic = 'Yes' if addicted_score > 18 or usage_hours > 6 else 'No'
        sleep_hours = max(3, min(10, 8 - (usage_hours // 2) + random.randint(-1, 1)))
        mental_health_score = max(1, min(10, 11 - (addicted_score // 3) + random.randint(-1, 1)))
        relationship_status = random.choice(relationship_statuses)
        conflicts = random.randint(0, 5) if addicted_score < 15 else random.randint(3, 10)
        
        # Final addictive label (Binary for classification)
        # We can predict Addicted_Score (Regression) or Status (Classification)
        # Let's say score > 19 is "Addicted"
        status = 1 if addicted_score >= 19 else 0
        
        data.append([
            age, gender, academic_level, country, usage_hours, platform,
            affects_academic, sleep_hours, mental_health_score, relationship_status,
            conflicts, addicted_score, status
        ])
    
    columns = [
        'Age', 'Gender', 'Academic_Level', 'Country', 'Avg_Daily_Usage_Hours', 
        'Most_Used_Platform', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 
        'Mental_Health_Score', 'Relationship_Status', 'Conflicts_Over_Social_Media', 
        'Addicted_Score', 'Status'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('social_media_addiction_data.csv', index=False)
    print("Dataset generated successfully!")

if __name__ == "__main__":
    generate_data()
