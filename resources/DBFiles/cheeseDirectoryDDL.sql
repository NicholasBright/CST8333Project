DROP TABLE IF EXISTS cheese;

CREATE TABLE cheese (
  cheese_id INT PRIMARY KEY AUTO_INCREMENT,
  cheese_name_en VARCHAR ( 50 ),
  cheese_name_fr VARCHAR ( 50 ),
  manufacturer_name_en VARCHAR ( 50 ),
  manufacturer_name_fr VARCHAR ( 50 ),
  manufacturer_prov_code CHAR ( 2 ),
  manufacturing_type_en VARCHAR ( 20 ),
  manufacturing_type_fr VARCHAR ( 20 ),
  website_en VARCHAR ( 70 ),
  website_fr VARCHAR ( 70 ),
  fat_content_percent INT,
  moisture_percent INT,
  particularities_en VARCHAR ( 200 ),
  particularities_fr VARCHAR ( 200 ),
  flavour_en VARCHAR ( 200 ),
  flavour_fr VARCHAR ( 200 ),
  characteristics_en VARCHAR ( 200 ),
  characteristics_fr VARCHAR ( 200 ),
  ripening_en VARCHAR ( 50 ),
  ripening_fr VARCHAR ( 50 ),
  organic VARCHAR ( 40 ),
  category_type_en VARCHAR ( 50 ),
  category_type_fr VARCHAR ( 50 ),
  milk_type_en VARCHAR ( 20 ),
  milk_type_fr VARCHAR ( 20 ),
  milk_treatmentType_en VARCHAR ( 20 ),
  milk_treatmentType_fr VARCHAR ( 20 ),
  rind_type_en VARCHAR ( 20 ),
  rind_type_fr VARCHAR ( 20 ),
  last_update_date DATE
);