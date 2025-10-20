"""
Scenario Building Calculation Engine
Handles climate stress testing calculations using sector-specific multipliers
"""

from typing import Dict, List, Tuple
from .models import PortfolioEntry, ScenarioResult, ScenarioResponse
import logging

logger = logging.getLogger(__name__)


class ScenarioEngine:
    """
    Engine for calculating climate stress testing scenarios
    """
    
    def __init__(self):
        # Sector-specific multipliers for transition and physical risks
        self.sector_multipliers = {
            "Power Generation – Fossil Fuel": {
                "transition_pd_multiplier": 1.6,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 10.0
            },
            "Power Generation – Renewable": {
                "transition_pd_multiplier": 0.9,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Industrial Manufacturing": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Transportation (Aviation & Shipping)": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Construction & Materials": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Real Estate (Commercial)": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 15.0
            },
            "Agriculture & Forestry": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Financial Services": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Power (Independent Producers)": {
                "transition_pd_multiplier": 1.5,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 10.0
            },
            "Manufacturing SMEs": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Transport & Logistics": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Real Estate (SME Developers)": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.3,
                "lgd_change": 15.0
            },
            "Agriculture / Food SMEs": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Oil & Gas (Upstream, Midstream, Downstream)": {
                "transition_pd_multiplier": 1.6,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 15.0
            },
            "Renewable Energy": {
                "transition_pd_multiplier": 0.9,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Infrastructure (Ports, Roads)": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.3,
                "lgd_change": 20.0
            },
            "Mining & Metals": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Residential Real Estate": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Commercial Real Estate": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 15.0
            },
            "Passenger Vehicles": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            "Heavy Transport": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Sovereign (Pakistan/UAE/etc.)": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.3,
                "lgd_change": 5.0
            },
            "Buildings (Urban)": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 15.0
            },
            # Additional mappings for sectors that might match
            "Steel & Iron": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Cement": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Chemicals & Petrochemicals": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Fertilizers": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Pulp & Paper": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Textile & Apparel": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Automotive & Transport Equipment": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            "Electronics & Machinery": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Aviation": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Shipping / Marine Transport": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Rail Transport": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Road Freight & Logistics": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Public Transport & Mobility": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Construction & Infrastructure": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Agriculture": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Livestock & Dairy": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Forestry & Logging": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Fisheries & Aquaculture": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Food Processing & Packaging": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Banking / Financial Services": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Insurance & Reinsurance": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Asset Management / Investment": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Retail & Consumer Goods": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            "Hospitality & Leisure": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Healthcare & Pharma": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            "Telecom & Data Centers": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Public Sector & Sovereign": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.3,
                "lgd_change": 5.0
            },
            "Technology (IT & Cloud)": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            # Add mappings for simple sector names from frontend
            "Energy": {
                "transition_pd_multiplier": 1.6,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 15.0
            },
            "Manufacturing": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 8.0
            },
            "Retail": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Technology": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            "Agriculture": {
                "transition_pd_multiplier": 1.2,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 20.0
            },
            "Real Estate": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.4,
                "lgd_change": 15.0
            },
            "Healthcare": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            },
            "Financial Services": {
                "transition_pd_multiplier": 1.0,
                "physical_pd_multiplier": 1.0,
                "lgd_change": 0.0
            },
            "Transportation": {
                "transition_pd_multiplier": 1.4,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 10.0
            },
            "Construction": {
                "transition_pd_multiplier": 1.3,
                "physical_pd_multiplier": 1.2,
                "lgd_change": 12.0
            },
            "Other": {
                "transition_pd_multiplier": 1.1,
                "physical_pd_multiplier": 1.1,
                "lgd_change": 5.0
            }
        }
    
    def get_sector_multipliers(self, sector: str) -> Dict[str, float]:
        """
        Get multipliers for a given sector
        Returns default values if sector not found
        """
        return self.sector_multipliers.get(sector, {
            "transition_pd_multiplier": 1.0,
            "physical_pd_multiplier": 1.0,
            "lgd_change": 0.0
        })
    
    def calculate_scenario(self, portfolio_entries: List[PortfolioEntry], scenario_type: str) -> ScenarioResponse:
        """
        Calculate climate stress testing scenario
        
        Formula: CAEL = Exposure × (Baseline PD × PD Multiplier) × (Baseline LGD + LGD Change)
        """
        try:
            logger.info(f"Starting scenario calculation for {len(portfolio_entries)} entries with scenario type: {scenario_type}")
            
            results = []
            total_exposure = 0.0
            total_baseline_expected_loss = 0.0
            total_climate_adjusted_expected_loss = 0.0
            
            for i, entry in enumerate(portfolio_entries):
                logger.info(f"Processing entry {i+1}: {entry.company} (Sector: {entry.sector}, Amount: {entry.amount})")
                # Get sector-specific multipliers
                multipliers = self.get_sector_multipliers(entry.sector)
                logger.info(f"  Using multipliers for {entry.sector}: {multipliers}")
                
                # Calculate PD multiplier based on scenario type
                if scenario_type == "transition":
                    pd_multiplier = multipliers["transition_pd_multiplier"]
                elif scenario_type == "physical":
                    pd_multiplier = multipliers["physical_pd_multiplier"]
                elif scenario_type == "combined":
                    pd_multiplier = multipliers["transition_pd_multiplier"] * multipliers["physical_pd_multiplier"]
                else:
                    raise ValueError(f"Invalid scenario type: {scenario_type}")
                
                # Convert percentages to decimals
                baseline_pd_decimal = entry.probability_of_default / 100.0
                baseline_lgd_decimal = entry.loss_given_default / 100.0
                lgd_change_decimal = multipliers["lgd_change"] / 100.0
                
                # Calculate adjusted values
                adjusted_pd = baseline_pd_decimal * pd_multiplier
                adjusted_lgd = baseline_lgd_decimal + lgd_change_decimal
                
                # Ensure LGD doesn't exceed 100%
                adjusted_lgd = min(adjusted_lgd, 1.0)
                
                # Calculate expected losses
                baseline_expected_loss = entry.amount * baseline_pd_decimal * baseline_lgd_decimal
                climate_adjusted_expected_loss = entry.amount * adjusted_pd * adjusted_lgd
                
                # Calculate increases
                loss_increase = climate_adjusted_expected_loss - baseline_expected_loss
                loss_increase_percentage = (loss_increase / baseline_expected_loss * 100.0) if baseline_expected_loss > 0 else 0.0
                
                # Create result
                result = ScenarioResult(
                    company=entry.company,
                    sector=entry.sector,
                    exposure=entry.amount,
                    baseline_pd=entry.probability_of_default,
                    baseline_lgd=entry.loss_given_default,
                    pd_multiplier=pd_multiplier,
                    adjusted_pd=adjusted_pd * 100.0,  # Convert back to percentage
                    lgd_change=multipliers["lgd_change"],
                    adjusted_lgd=adjusted_lgd * 100.0,  # Convert back to percentage
                    climate_adjusted_expected_loss=climate_adjusted_expected_loss,
                    baseline_expected_loss=baseline_expected_loss,
                    loss_increase=loss_increase,
                    loss_increase_percentage=loss_increase_percentage
                )
                
                results.append(result)
                
                # Accumulate totals
                total_exposure += entry.amount
                total_baseline_expected_loss += baseline_expected_loss
                total_climate_adjusted_expected_loss += climate_adjusted_expected_loss
            
            # Calculate total increases
            total_loss_increase = total_climate_adjusted_expected_loss - total_baseline_expected_loss
            total_loss_increase_percentage = (total_loss_increase / total_baseline_expected_loss * 100.0) if total_baseline_expected_loss > 0 else 0.0
            
            return ScenarioResponse(
                success=True,
                scenario_type=scenario_type,
                total_exposure=total_exposure,
                total_baseline_expected_loss=total_baseline_expected_loss,
                total_climate_adjusted_expected_loss=total_climate_adjusted_expected_loss,
                total_loss_increase=total_loss_increase,
                total_loss_increase_percentage=total_loss_increase_percentage,
                results=results
            )
            
        except Exception as e:
            logger.error(f"Error calculating scenario: {str(e)}")
            return ScenarioResponse(
                success=False,
                scenario_type=scenario_type,
                total_exposure=0.0,
                total_baseline_expected_loss=0.0,
                total_climate_adjusted_expected_loss=0.0,
                total_loss_increase=0.0,
                total_loss_increase_percentage=0.0,
                results=[],
                error=str(e)
            )
