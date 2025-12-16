-- Create scoping_submissions table
CREATE TABLE IF NOT EXISTS scoping_submissions (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    scoping_data JSONB NOT NULL,
    selected_roles JSONB NOT NULL,
    comments TEXT,
    submitted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'PENDING',
    calculation_result JSONB,
    calculated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_scoping_submissions_user_email ON scoping_submissions(user_email);
CREATE INDEX idx_scoping_submissions_status ON scoping_submissions(status);
CREATE INDEX idx_scoping_submissions_submitted_at ON scoping_submissions(submitted_at DESC);

-- Add comments to table
COMMENT ON TABLE scoping_submissions IS 'Stores FCCS scoping tool submissions and calculation results';
COMMENT ON COLUMN scoping_submissions.scoping_data IS 'JSON object containing all form data from the scoping tool';
COMMENT ON COLUMN scoping_submissions.selected_roles IS 'JSON array of selected roles for the project';
COMMENT ON COLUMN scoping_submissions.calculation_result IS 'JSON object with calculation results from backend (weeks, complexity, cost, breakdown, etc.)';
COMMENT ON COLUMN scoping_submissions.status IS 'Status: PENDING, COMPLETED, FAILED';
