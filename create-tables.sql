-- 1. Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- -----------------------------------------------------
-- 2. Customers Table (Core Identity & Unique Subscription Guard)
-- -----------------------------------------------------
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    preferred_name VARCHAR(100), -- Used for friendly email salutations
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    cre_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updt_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),

    CONSTRAINT uq_customer_identity UNIQUE (first_name, last_name, email)
);

-- faster lookup for email addresses
CREATE INDEX idx_customers_email ON customers(email);


-- -----------------------------------------------------
-- 3. Customer Preferences Table (Subscription Settings)
-- -----------------------------------------------------
CREATE TABLE customer_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    profile_name VARCHAR(100) DEFAULT 'Default Profile', --Allows customers to have multiple profiles - "Summer Weight Loss", "Post-Workout Bulk", "Weekend Detox"
    days INT DEFAULT 7,
    max_calories INT DEFAULT 500,
    nut_free BOOLEAN DEFAULT FALSE,
    gluten_free BOOLEAN DEFAULT FALSE,
    dairy_free BOOLEAN DEFAULT FALSE,
    soy_free BOOLEAN DEFAULT FALSE,
    cre_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updt_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);


CREATE INDEX idx_customer_preferences_customer_id ON customer_preferences(customer_id);


-- -----------------------------------------------------
-- 4. Recipe History Table (References Customer ID)
-- -----------------------------------------------------
CREATE TABLE recipe_history (
   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    recipe_name VARCHAR(255) NOT NULL,
    day_number INT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    calories INT,
    embedding vector(1536), 
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

CREATE INDEX recipe_embedding_hnsw_idx ON recipe_history USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_recipe_history_customer ON recipe_history(customer_id);
CREATE INDEX idx_recipe_history_customer_day ON recipe_history(customer_id, day_number);


-- -----------------------------------------------------
-- 5. Motivational Quotes Master Table (Common LLM Lookup)
-- -----------------------------------------------------
CREATE TABLE motivational_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(50) DEFAULT 'Weight Loss', -- e.g., 'Weight Loss', 'Energy', 'General Wellness'
    message TEXT NOT NULL,
    cre_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

-- -----------------------------------------------------
-- 6. Customer Quote History Table (Tracks Sent Messages to Prevent Repeats)
-- -----------------------------------------------------
CREATE TABLE customer_quote_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    quote_id UUID REFERENCES motivational_quotes(id) ON DELETE CASCADE,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    
    -- Ensures a specific quote is never sent to the same customer twice
    CONSTRAINT uq_customer_quote UNIQUE (customer_id, quote_id)
);

CREATE INDEX idx_customer_quote_history ON customer_quote_history(customer_id, quote_id);

-- -----------------------------------------------------
-- 7. Workflow Runs Table
-- -----------------------------------------------------
CREATE TABLE workflow_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',   -- -- PENDING, RUNNING, SUCCESS, FAILED
    attempt_count int DEFAULT 0, -- -- Tracks how many tries have occurred (max 3)            
    validation_errors TEXT, -- -- Captures the terminal exception or reason for failure
    email_status VARCHAR(50) DEFAULT 'PENDING', -- -- PENDING, SENT, FAILED                 
    started_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);
CREATE INDEX idx_workflow_runs_customer ON workflow_runs(customer_id);
CREATE INDEX idx_workflow_runs_status ON workflow_runs(status);

-- -----------------------------------------------------
-- 8. Subscriptions Table (Tracks Plan Status & Lifecycles)
-- -----------------------------------------------------
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    plan_name VARCHAR(100) NOT NULL DEFAULT 'Standard Smoothie Plan', 
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',                      
    start_date DATE DEFAULT (CURRENT_DATE),
    end_date DATE,                                 
    cre_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updt_ts TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

CREATE INDEX idx_subscriptions_customer_id ON subscriptions(customer_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

