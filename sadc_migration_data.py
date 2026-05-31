"""
sadc_migration_data.py
Track Zimbabwean migration rates and diaspora populations across SADC countries
Includes:
- Migration flows by destination country
- Diaspora population estimates
- Border crossing data
- Remittance patterns
- Refugee and asylum seeker trends
- Occupational profiles
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# SADC Member Countries
SADC_COUNTRIES = {
    'South Africa': {'code': 'ZA', 'region': 'Southern', 'primary_destination': True},
    'Botswana': {'code': 'BW', 'region': 'Southern', 'primary_destination': True},
    'Zambia': {'code': 'ZM', 'region': 'Northern', 'primary_destination': True},
    'Mozambique': {'code': 'MZ', 'region': 'Eastern', 'primary_destination': False},
    'Malawi': {'code': 'MW', 'region': 'Eastern', 'primary_destination': False},
    'Tanzania': {'code': 'TZ', 'region': 'Eastern', 'primary_destination': False},
    'Angola': {'code': 'AO', 'region': 'Western', 'primary_destination': False},
    'DRC': {'code': 'CD', 'region': 'Western', 'primary_destination': False},
    'Namibia': {'code': 'NA', 'region': 'Southern', 'primary_destination': False},
    'Lesotho': {'code': 'LS', 'region': 'Southern', 'primary_destination': False},
    'Eswatini': {'code': 'SZ', 'region': 'Southern', 'primary_destination': False},
    'Madagascar': {'code': 'MG', 'region': 'Island', 'primary_destination': False},
    'Mauritius': {'code': 'MU', 'region': 'Island', 'primary_destination': False},
}

def generate_sadc_migration_data(start_year=2010, end_year=2024):
    """
    Generate realistic Zimbabwean migration data across SADC countries
    Based on known migration patterns and patterns
    """
    
    records = []
    np.random.seed(42)
    
    years = np.arange(start_year, end_year + 1)
    
    # Base population estimates (2024) for Zimbabwean diaspora by country
    base_diaspora = {
        'South Africa': 1200000,      # Largest Zimbabwean diaspora
        'Botswana': 450000,           # Second largest
        'Zambia': 380000,             # Third largest
        'Mozambique': 220000,
        'UK': 180000,                 # Outside SADC but major destination
        'USA': 150000,
        'Malawi': 95000,
        'Tanzania': 85000,
        'Namibia': 45000,
        'Angola': 38000,
        'Eswatini': 28000,
        'Lesotho': 15000,
        'Australia': 75000,
        'Canada': 65000,
    }
    
    # Migration intensities (annual out-migration rates %)
    migration_rates = {
        'South Africa': {'base': 3.5, 'trend': 0.15},      # High but stable
        'Botswana': {'base': 2.1, 'trend': 0.08},
        'Zambia': {'base': 1.8, 'trend': 0.06},
        'Mozambique': {'base': 0.9, 'trend': 0.03},
        'UK': {'base': 0.8, 'trend': 0.04},
        'USA': {'base': 0.7, 'trend': 0.05},
        'Malawi': {'base': 0.5, 'trend': 0.02},
        'Tanzania': {'base': 0.45, 'trend': 0.02},
        'Namibia': {'base': 0.25, 'trend': 0.01},
        'Angola': {'base': 0.20, 'trend': 0.01},
    }
    
    # Generate data for each year and destination
    for country in SADC_COUNTRIES.keys():
        for year in years:
            year_factor = (year - start_year) / (end_year - start_year)
            
            # Get base migration rate (defaults to 0.15% if not specified)
            rate_info = migration_rates.get(country, {'base': 0.15, 'trend': 0.01})
            base_rate = rate_info['base']
            trend = rate_info['trend']
            
            # Calculate migration rate with trend
            current_rate = base_rate + trend * year_factor + np.random.normal(0, 0.1)
            current_rate = max(0, min(5.0, current_rate))  # Clamp between 0-5%
            
            # Estimate population
            base_pop = base_diaspora.get(country, 10000)
            current_pop = base_pop * (1 + (current_rate / 100)) ** (year - start_year)
            
            # Additional metrics
            occupations = get_occupation_distribution(country, current_rate)
            remittance_amount = estimate_remittances(current_pop, country)
            border_crossings = estimate_border_activity(country, current_rate)
            
            records.append({
                'year': year,
                'destination_country': country,
                'region': SADC_COUNTRIES[country]['region'],
                'annual_migration_rate': current_rate,
                'estimated_diaspora_population': current_pop,
                'male_percentage': np.random.normal(48, 2),  # Slightly more women migrate
                'employment_rate': np.random.normal(0.72, 0.05),  # Employment rate
                'unemployment_rate': np.random.normal(0.15, 0.04),
                'self_employed_percentage': np.random.normal(0.25, 0.08),
                'remittances_usd_millions': remittance_amount,
                'border_crossings_annual': border_crossings,
                'refugees_asylum_seekers': estimate_vulnerable_population(country, current_pop),
                'students_professionals': estimate_high_skill_migrants(country, current_rate),
                'irregular_migrants_pct': estimate_irregular_percentage(country),
                'family_reunification_pct': estimate_family_reunification(country),
                'return_migration_pct': estimate_return_migration(year, country),
                'hub_country': SADC_COUNTRIES[country]['primary_destination'],
                'documentation_rate': estimate_documentation_rate(country),
                'average_stay_years': estimate_average_stay(country),
            })
    
    df = pd.DataFrame(records)
    return df


def get_occupation_distribution(country, migration_rate):
    """Get typical occupation distribution for Zimbabweans in destination country"""
    occupations = {
        'South Africa': {'healthcare': 0.18, 'construction': 0.22, 'domestic_work': 0.25, 
                        'retail': 0.15, 'professional': 0.12, 'other': 0.08},
        'Botswana': {'construction': 0.28, 'mining': 0.18, 'professional': 0.20,
                    'retail': 0.18, 'hospitality': 0.12, 'other': 0.04},
        'Zambia': {'mining': 0.35, 'agriculture': 0.25, 'professional': 0.15,
                  'construction': 0.15, 'retail': 0.08, 'other': 0.02},
    }
    return occupations.get(country, {'professional': 0.2, 'skilled': 0.3, 'unskilled': 0.5})


def estimate_remittances(population, country):
    """Estimate annual remittances (USD millions) based on diaspora population"""
    # Average annual remittance per migrant varies by country
    remittance_per_capita = {
        'South Africa': 450,        # USD per year
        'Botswana': 550,
        'Zambia': 350,
        'Mozambique': 280,
        'UK': 1200,                 # Higher for developed countries
        'USA': 1400,
        'Malawi': 250,
        'Tanzania': 300,
    }
    
    per_capita = remittance_per_capita.get(country, 400)
    total = (population * per_capita) / 1_000_000  # Convert to millions
    # Add noise
    total *= np.random.uniform(0.85, 1.15)
    return max(0, total)


def estimate_border_activity(country, migration_rate):
    """Estimate annual border crossings to/from destination"""
    # Border crossing base rates
    crossings_per_migrant = {
        'South Africa': 2.5,        # Frequent back-and-forth
        'Botswana': 2.2,
        'Zambia': 2.0,
        'Mozambique': 1.8,
        'Malawi': 1.5,
    }
    
    # Assume 50% diaspora population crosses borders in a year
    crossings_per_capita = crossings_per_migrant.get(country, 1.2)
    base_crossings = 200000 + migration_rate * 50000  # Baseline + migration-dependent
    return int(base_crossings * (1 + np.random.normal(0, 0.2)))


def estimate_vulnerable_population(country, population):
    """Estimate refugees and asylum seekers percentage"""
    vulnerable_rates = {
        'Botswana': 0.05,
        'South Africa': 0.03,
        'Zambia': 0.08,
        'Tanzania': 0.12,
        'Mozambique': 0.06,
    }
    
    rate = vulnerable_rates.get(country, 0.02)
    return int(population * rate)


def estimate_high_skill_migrants(country, migration_rate):
    """Estimate number of students and professionals"""
    skill_rates = {
        'UK': 0.35,         # High proportion of students/professionals
        'USA': 0.38,
        'South Africa': 0.12,
        'Botswana': 0.15,
        'Australia': 0.40,
    }
    
    rate = skill_rates.get(country, 0.08)
    population_estimate = 50000 + migration_rate * 30000
    return int(population_estimate * rate)


def estimate_irregular_percentage(country):
    """Estimate percentage of irregular/undocumented migrants"""
    irregular_rates = {
        'South Africa': 0.45,
        'Botswana': 0.25,
        'Zambia': 0.35,
        'Mozambique': 0.40,
        'Malawi': 0.30,
        'UK': 0.08,
        'USA': 0.12,
    }
    
    return irregular_rates.get(country, 0.20)


def estimate_family_reunification(country):
    """Percentage of migrants who brought family members"""
    family_rates = {
        'South Africa': 0.35,
        'Botswana': 0.25,
        'Zambia': 0.20,
        'UK': 0.40,
        'USA': 0.45,
    }
    
    return family_rates.get(country, 0.18)


def estimate_return_migration(year, country):
    """Estimate return migration percentage (those leaving the country)"""
    # Return rates vary; generally 5-15% return annually
    base_return = {
        'South Africa': 0.08,
        'Botswana': 0.06,
        'Zambia': 0.12,
        'UK': 0.04,
        'USA': 0.03,
    }
    
    rate = base_return.get(country, 0.07)
    # Economic crises increase returns
    if year in [2020, 2021]:  # COVID period
        rate *= 1.3
    
    return rate + np.random.normal(0, 0.02)


def estimate_documentation_rate(country):
    """Estimate percentage with proper documentation"""
    doc_rates = {
        'South Africa': 0.55,
        'Botswana': 0.75,
        'Zambia': 0.65,
        'UK': 0.92,
        'USA': 0.88,
    }
    
    return doc_rates.get(country, 0.50)


def estimate_average_stay(country):
    """Average years stayed in destination country"""
    stay_years = {
        'South Africa': 8.5,
        'Botswana': 7.2,
        'Zambia': 6.8,
        'UK': 12.3,
        'USA': 13.1,
        'Mozambique': 5.2,
    }
    
    return stay_years.get(country, 6.0)


def generate_sadc_sector_employment():
    """Generate employment sector breakdown for Zimbabwean diaspora by country"""
    
    sectors = {
        'South Africa': {
            'Healthcare & Social': 0.18,
            'Construction & Real Estate': 0.22,
            'Domestic & Personal Services': 0.25,
            'Retail & Hospitality': 0.15,
            'Professional Services': 0.12,
            'Manufacturing': 0.05,
            'Agriculture': 0.03,
        },
        'Botswana': {
            'Mining & Resources': 0.18,
            'Construction': 0.28,
            'Professional Services': 0.20,
            'Retail & Hospitality': 0.18,
            'Agriculture': 0.12,
            'Manufacturing': 0.04,
        },
        'Zambia': {
            'Mining': 0.35,
            'Agriculture': 0.25,
            'Professional Services': 0.15,
            'Construction': 0.15,
            'Retail': 0.08,
            'Manufacturing': 0.02,
        },
        'UK': {
            'Healthcare': 0.28,
            'Professional Services': 0.25,
            'Education': 0.15,
            'Finance': 0.12,
            'Retail': 0.10,
            'Other': 0.10,
        },
        'USA': {
            'Healthcare': 0.22,
            'Technology & IT': 0.18,
            'Professional Services': 0.20,
            'Finance': 0.15,
            'Education': 0.12,
            'Other': 0.13,
        }
    }
    
    return sectors


def export_sadc_migration_data(df, format='csv'):
    """Export SADC migration data to file"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == 'csv':
        filepath = data_dir / f'zimbabwean_sadc_migration_{timestamp}.csv'
        df.to_csv(filepath, index=False)
    elif format == 'excel':
        filepath = data_dir / f'zimbabwean_sadc_migration_{timestamp}.xlsx'
        df.to_excel(filepath, index=False)
    elif format == 'json':
        filepath = data_dir / f'zimbabwean_sadc_migration_{timestamp}.json'
        df.to_json(filepath, orient='records', indent=2)
    
    print(f"✓ Data exported to: {filepath}")
    return filepath


def generate_regional_summary(df):
    """Generate summary statistics by region"""
    
    summary = df[df['year'] == df['year'].max()].groupby('region').agg({
        'estimated_diaspora_population': 'sum',
        'annual_migration_rate': 'mean',
        'remittances_usd_millions': 'sum',
        'destination_country': 'count'
    }).round(2)
    
    summary.columns = ['Total Diaspora', 'Avg Migration Rate %', 'Total Remittances $M', 'Countries']
    
    return summary


if __name__ == "__main__":
    print("=" * 80)
    print("ZIMBABWEAN SADC MIGRATION DATA GENERATION")
    print("=" * 80)
    
    # Generate main dataset
    print("\n[1/3] Generating SADC migration data (2010-2024)...")
    sadc_df = generate_sadc_migration_data()
    print(f"✓ Generated {len(sadc_df)} records across {sadc_df['destination_country'].nunique()} countries")
    
    # Export to CSV
    print("\n[2/3] Exporting data...")
    filepath = export_sadc_migration_data(sadc_df, format='csv')
    print(f"✓ Exported to: {filepath}")
    
    # Generate summary
    print("\n[3/3] Regional Summary Statistics:")
    summary = generate_regional_summary(sadc_df)
    print(summary)
    
    print("\n" + "=" * 80)
    print("✓ SADC Migration Dataset Created Successfully")
    print("=" * 80)
