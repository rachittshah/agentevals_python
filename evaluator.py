"""
Evaluation framework for AgentEval using Selenium for testing.
This replaces the original Cypress testing implementation.
"""

import os
import json
import shutil
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Evaluator:
    """Evaluator that tests agent-modified code using Selenium."""
    
    def __init__(self, output_dir: str = "./output"):
        """
        Initialize the evaluator.
        
        Args:
            output_dir: Directory to store evaluation results
        """
        self.output_dir = output_dir
        
    def setup_webdriver(self):
        """Set up and return a Chrome webdriver for testing."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    def run_test(self, eval_id: str, eval_dir: str) -> bool:
        """
        Run a test for a specific evaluation.
        
        Args:
            eval_id: Identifier for the evaluation
            eval_dir: Directory containing the modified code
            
        Returns:
            True if test passes, False otherwise
        """
        try:
            driver = self.setup_webdriver()
            
            # Create file URL
            file_path = os.path.join(eval_dir, "index.html")
            file_url = f"file://{os.path.abspath(file_path)}"
            
            # Navigate to the page
            driver.get(file_url)
            
            # Test the counter functionality
            count_element = driver.find_element(By.ID, "count")
            assert count_element.text == "0", "Initial count should be 0"
            
            # Click the increment button
            increment_button = driver.find_element(By.ID, "incrementBtn")
            increment_button.click()
            
            # Wait for the count to update and verify
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, "count"), "1")
            )
            
            # Cleanup
            driver.quit()
            
            logger.info(f"[{eval_id}] Test passed")
            return True
            
        except Exception as e:
            logger.error(f"[{eval_id}] Test failed: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            return False
            
    def generate_results_html(self, results: dict) -> str:
        """
        Generate HTML to visualize test results.
        
        Args:
            results: Dictionary mapping eval_id to test result (True/False)
            
        Returns:
            HTML string representing the results
        """
        html = "<html><head><title>AgentEval Results</title></head><body>"
        html += "<h1>AgentEval Results</h1>"
        html += "<div style='display: flex; flex-wrap: wrap;'>"
        
        for key, value in results.items():
            box_color = "green" if value else "red"
            html += f"<div style='background-color: {box_color}; width: 50px; height: 50px; display: inline-block; margin: 5px; border: 2px solid #333;'>{key}</div>"
        
        html += "</div></body></html>"
        return html
