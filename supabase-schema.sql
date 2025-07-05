-- Growth Accelerator Platform - Supabase Database Schema
-- Run this in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Candidates table
CREATE TABLE candidates (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  workable_id TEXT UNIQUE,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  phone TEXT,
  skills JSONB DEFAULT '[]'::jsonb,
  experience_years INTEGER,
  location TEXT,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'hired', 'blacklisted')),
  applications_count INTEGER DEFAULT 0,
  resume_url TEXT,
  linkedin_url TEXT,
  portfolio_url TEXT,
  salary_expectation INTEGER,
  availability TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Jobs table
CREATE TABLE jobs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  workable_id TEXT UNIQUE,
  title TEXT NOT NULL,
  company TEXT,
  location TEXT,
  description TEXT,
  requirements JSONB DEFAULT '[]'::jsonb,
  skills_required JSONB DEFAULT '[]'::jsonb,
  salary_min INTEGER,
  salary_max INTEGER,
  employment_type TEXT DEFAULT 'full-time' CHECK (employment_type IN ('full-time', 'part-time', 'contract', 'internship')),
  remote_allowed BOOLEAN DEFAULT false,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'closed', 'draft')),
  applications_count INTEGER DEFAULT 0,
  department TEXT,
  seniority_level TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Applications table
CREATE TABLE applications (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  candidate_id UUID REFERENCES candidates(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'reviewing', 'interviewing', 'offered', 'hired', 'rejected', 'withdrawn')),
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  notes TEXT,
  score INTEGER CHECK (score >= 0 AND score <= 100),
  interview_date TIMESTAMP WITH TIME ZONE,
  salary_offered INTEGER,
  feedback TEXT,
  stage TEXT DEFAULT 'application',
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(candidate_id, job_id)
);

-- Clients table (companies using the platform)
CREATE TABLE clients (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  company TEXT,
  industry TEXT,
  size_category TEXT,
  location TEXT,
  website TEXT,
  description TEXT,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Consultants table (internal staff)
CREATE TABLE consultants (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  specialization TEXT,
  active BOOLEAN DEFAULT true,
  performance_score INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Skills table
CREATE TABLE skills (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  category TEXT,
  demand_level INTEGER DEFAULT 1 CHECK (demand_level >= 1 AND demand_level <= 5),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Job skills junction table
CREATE TABLE job_skills (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
  required BOOLEAN DEFAULT true,
  importance_level INTEGER DEFAULT 3 CHECK (importance_level >= 1 AND importance_level <= 5),
  UNIQUE(job_id, skill_id)
);

-- Candidate skills junction table
CREATE TABLE candidate_skills (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  candidate_id UUID REFERENCES candidates(id) ON DELETE CASCADE,
  skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
  proficiency_level INTEGER DEFAULT 3 CHECK (proficiency_level >= 1 AND proficiency_level <= 5),
  years_experience INTEGER DEFAULT 0,
  UNIQUE(candidate_id, skill_id)
);

-- Placements table (successful hires)
CREATE TABLE placements (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  application_id UUID REFERENCES applications(id),
  consultant_id UUID REFERENCES consultants(id),
  client_id UUID REFERENCES clients(id),
  start_date DATE,
  end_date DATE,
  salary INTEGER,
  placement_fee INTEGER,
  commission_rate DECIMAL(5,2),
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'terminated')),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI matching results table
CREATE TABLE ai_matches (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  candidate_id UUID REFERENCES candidates(id),
  job_id UUID REFERENCES jobs(id),
  match_score INTEGER CHECK (match_score >= 0 AND match_score <= 100),
  reasoning JSONB,
  suggested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  status TEXT DEFAULT 'suggested' CHECK (status IN ('suggested', 'reviewed', 'accepted', 'rejected'))
);

-- Activity log table
CREATE TABLE activity_log (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  action TEXT NOT NULL,
  details JSONB,
  user_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_status ON candidates(status);
CREATE INDEX idx_candidates_workable_id ON candidates(workable_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_workable_id ON jobs(workable_id);
CREATE INDEX idx_applications_candidate_id ON applications(candidate_id);
CREATE INDEX idx_applications_job_id ON applications(job_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_ai_matches_candidate_id ON ai_matches(candidate_id);
CREATE INDEX idx_ai_matches_job_id ON ai_matches(job_id);
CREATE INDEX idx_ai_matches_score ON ai_matches(match_score DESC);
CREATE INDEX idx_activity_log_entity ON activity_log(entity_type, entity_id);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_consultants_updated_at BEFORE UPDATE ON consultants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_placements_updated_at BEFORE UPDATE ON placements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security
ALTER TABLE candidates ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultants ENABLE ROW LEVEL SECURITY;
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE candidate_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE placements ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_log ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Allow all operations for authenticated users (can be restricted later)
CREATE POLICY "Allow all operations on candidates" ON candidates FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on jobs" ON jobs FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on applications" ON applications FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on clients" ON clients FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on consultants" ON consultants FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on skills" ON skills FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on job_skills" ON job_skills FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on candidate_skills" ON candidate_skills FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on placements" ON placements FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on ai_matches" ON ai_matches FOR ALL TO authenticated USING (true);
CREATE POLICY "Allow all operations on activity_log" ON activity_log FOR ALL TO authenticated USING (true);

-- Public read access for some tables (for the standalone React component)
CREATE POLICY "Allow public read on candidates" ON candidates FOR SELECT TO anon USING (true);
CREATE POLICY "Allow public read on jobs" ON jobs FOR SELECT TO anon USING (true);
CREATE POLICY "Allow public read on applications" ON applications FOR SELECT TO anon USING (true);
CREATE POLICY "Allow public read on skills" ON skills FOR SELECT TO anon USING (true);

-- Enable real-time subscriptions
ALTER PUBLICATION supabase_realtime ADD TABLE candidates;
ALTER PUBLICATION supabase_realtime ADD TABLE jobs;
ALTER PUBLICATION supabase_realtime ADD TABLE applications;
ALTER PUBLICATION supabase_realtime ADD TABLE ai_matches;

-- Insert some initial skills data
INSERT INTO skills (name, category, demand_level) VALUES
('JavaScript', 'Programming', 5),
('Python', 'Programming', 5),
('React', 'Frontend', 5),
('Node.js', 'Backend', 4),
('PostgreSQL', 'Database', 4),
('AWS', 'Cloud', 4),
('Docker', 'DevOps', 3),
('Machine Learning', 'AI/ML', 4),
('Project Management', 'Management', 3),
('Leadership', 'Management', 3),
('Communication', 'Soft Skills', 5),
('Problem Solving', 'Soft Skills', 5);