// Growth Accelerator Platform - AI Matching Edge Function
// Supabase Edge Function for intelligent candidate-job matching

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface MatchingRequest {
  candidate_id?: string
  job_id?: string
  limit?: number
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Initialize Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
    )

    const { candidate_id, job_id, limit = 10 }: MatchingRequest = await req.json()

    let matches = []

    if (candidate_id && !job_id) {
      // Find matching jobs for a candidate
      matches = await findJobsForCandidate(supabaseClient, candidate_id, limit)
    } else if (job_id && !candidate_id) {
      // Find matching candidates for a job
      matches = await findCandidatesForJob(supabaseClient, job_id, limit)
    } else if (candidate_id && job_id) {
      // Calculate match score for specific candidate-job pair
      matches = await calculateSpecificMatch(supabaseClient, candidate_id, job_id)
    } else {
      // Generate general matching suggestions
      matches = await generateGeneralMatches(supabaseClient, limit)
    }

    return new Response(
      JSON.stringify({
        success: true,
        matches,
        count: matches.length,
        timestamp: new Date().toISOString(),
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      },
    )

  } catch (error) {
    console.error('AI Matching error:', error)

    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
        timestamp: new Date().toISOString(),
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      },
    )
  }
})

async function findJobsForCandidate(supabaseClient: any, candidateId: string, limit: number) {
  // Get candidate details with skills
  const { data: candidate, error: candidateError } = await supabaseClient
    .from('candidates')
    .select(`
      *,
      candidate_skills (
        skill_id,
        proficiency_level,
        skills (name, category)
      )
    `)
    .eq('id', candidateId)
    .single()

  if (candidateError || !candidate) {
    throw new Error('Candidate not found')
  }

  // Get all active jobs with their required skills
  const { data: jobs, error: jobsError } = await supabaseClient
    .from('jobs')
    .select(`
      *,
      job_skills (
        skill_id,
        required,
        importance_level,
        skills (name, category)
      )
    `)
    .eq('status', 'active')

  if (jobsError) {
    throw new Error('Failed to fetch jobs')
  }

  // Calculate match scores
  const matches = jobs.map(job => {
    const score = calculateMatchScore(candidate, job)
    const reasoning = generateMatchReasoning(candidate, job, score)
    
    return {
      job,
      candidate,
      match_score: score,
      reasoning,
      match_type: 'candidate_to_jobs'
    }
  })

  // Sort by match score and return top matches
  return matches
    .sort((a, b) => b.match_score - a.match_score)
    .slice(0, limit)
}

async function findCandidatesForJob(supabaseClient: any, jobId: string, limit: number) {
  // Get job details with required skills
  const { data: job, error: jobError } = await supabaseClient
    .from('jobs')
    .select(`
      *,
      job_skills (
        skill_id,
        required,
        importance_level,
        skills (name, category)
      )
    `)
    .eq('id', jobId)
    .single()

  if (jobError || !job) {
    throw new Error('Job not found')
  }

  // Get all active candidates with their skills
  const { data: candidates, error: candidatesError } = await supabaseClient
    .from('candidates')
    .select(`
      *,
      candidate_skills (
        skill_id,
        proficiency_level,
        skills (name, category)
      )
    `)
    .eq('status', 'active')

  if (candidatesError) {
    throw new Error('Failed to fetch candidates')
  }

  // Calculate match scores
  const matches = candidates.map(candidate => {
    const score = calculateMatchScore(candidate, job)
    const reasoning = generateMatchReasoning(candidate, job, score)
    
    return {
      job,
      candidate,
      match_score: score,
      reasoning,
      match_type: 'job_to_candidates'
    }
  })

  // Sort by match score and return top matches
  return matches
    .sort((a, b) => b.match_score - a.match_score)
    .slice(0, limit)
}

async function calculateSpecificMatch(supabaseClient: any, candidateId: string, jobId: string) {
  // Get both candidate and job with skills
  const [candidateResult, jobResult] = await Promise.all([
    supabaseClient
      .from('candidates')
      .select(`
        *,
        candidate_skills (
          skill_id,
          proficiency_level,
          skills (name, category)
        )
      `)
      .eq('id', candidateId)
      .single(),
    
    supabaseClient
      .from('jobs')
      .select(`
        *,
        job_skills (
          skill_id,
          required,
          importance_level,
          skills (name, category)
        )
      `)
      .eq('id', jobId)
      .single()
  ])

  if (candidateResult.error || jobResult.error) {
    throw new Error('Candidate or job not found')
  }

  const candidate = candidateResult.data
  const job = jobResult.data

  const score = calculateMatchScore(candidate, job)
  const reasoning = generateMatchReasoning(candidate, job, score)

  // Store the match result
  await supabaseClient
    .from('ai_matches')
    .upsert({
      candidate_id: candidateId,
      job_id: jobId,
      match_score: score,
      reasoning,
      status: 'suggested'
    })

  return [{
    job,
    candidate,
    match_score: score,
    reasoning,
    match_type: 'specific_match'
  }]
}

async function generateGeneralMatches(supabaseClient: any, limit: number) {
  // Get top candidates and jobs for general matching
  const [candidatesResult, jobsResult] = await Promise.all([
    supabaseClient
      .from('candidates')
      .select(`
        *,
        candidate_skills (
          skill_id,
          proficiency_level,
          skills (name, category)
        )
      `)
      .eq('status', 'active')
      .limit(50),
    
    supabaseClient
      .from('jobs')
      .select(`
        *,
        job_skills (
          skill_id,
          required,
          importance_level,
          skills (name, category)
        )
      `)
      .eq('status', 'active')
      .limit(20)
  ])

  if (candidatesResult.error || jobsResult.error) {
    throw new Error('Failed to fetch data for general matching')
  }

  const candidates = candidatesResult.data
  const jobs = jobsResult.data

  const matches = []

  // Generate matches for each job with best candidates
  for (const job of jobs) {
    const jobMatches = candidates.map(candidate => {
      const score = calculateMatchScore(candidate, job)
      const reasoning = generateMatchReasoning(candidate, job, score)
      
      return {
        job,
        candidate,
        match_score: score,
        reasoning,
        match_type: 'general_suggestions'
      }
    })

    // Add top 3 matches for this job
    const topMatches = jobMatches
      .sort((a, b) => b.match_score - a.match_score)
      .slice(0, 3)
      .filter(match => match.match_score >= 60) // Only good matches

    matches.push(...topMatches)
  }

  // Return top overall matches
  return matches
    .sort((a, b) => b.match_score - a.match_score)
    .slice(0, limit)
}

function calculateMatchScore(candidate: any, job: any): number {
  let score = 0
  const factors = []

  // Skills matching (40% of score)
  const candidateSkills = candidate.candidate_skills?.map(cs => cs.skills?.name?.toLowerCase()) || []
  const jobSkills = job.job_skills?.map(js => js.skills?.name?.toLowerCase()) || []
  
  if (jobSkills.length > 0) {
    const matchingSkills = candidateSkills.filter(skill => jobSkills.includes(skill))
    const skillsScore = (matchingSkills.length / jobSkills.length) * 40
    score += skillsScore
    factors.push(`Skills: ${skillsScore.toFixed(1)}/40`)
  }

  // Experience level matching (25% of score)
  const candidateExp = candidate.experience_years || 0
  const requiredExp = extractExperienceFromJob(job)
  
  let expScore = 0
  if (requiredExp > 0) {
    if (candidateExp >= requiredExp) {
      expScore = 25 // Perfect match
    } else if (candidateExp >= requiredExp * 0.7) {
      expScore = 20 // Close match
    } else if (candidateExp >= requiredExp * 0.5) {
      expScore = 15 // Decent match
    } else {
      expScore = 5 // Poor match but some experience
    }
  } else {
    expScore = 15 // No specific requirement
  }
  
  score += expScore
  factors.push(`Experience: ${expScore}/25`)

  // Location matching (15% of score)
  const locationScore = calculateLocationScore(candidate.location, job.location, job.remote_allowed)
  score += locationScore
  factors.push(`Location: ${locationScore}/15`)

  // Salary expectations (10% of score)
  const salaryScore = calculateSalaryScore(candidate.salary_expectation, job.salary_min, job.salary_max)
  score += salaryScore
  factors.push(`Salary: ${salaryScore}/10`)

  // Availability (10% of score)
  const availabilityScore = candidate.status === 'active' ? 10 : 0
  score += availabilityScore
  factors.push(`Availability: ${availabilityScore}/10`)

  return Math.round(Math.min(score, 100))
}

function generateMatchReasoning(candidate: any, job: any, score: number): any {
  const candidateSkills = candidate.candidate_skills?.map(cs => cs.skills?.name) || []
  const jobSkills = job.job_skills?.map(js => js.skills?.name) || []
  const matchingSkills = candidateSkills.filter(skill => 
    jobSkills.some(jobSkill => jobSkill.toLowerCase() === skill.toLowerCase())
  )

  return {
    overall_score: score,
    matching_skills: matchingSkills,
    candidate_experience: candidate.experience_years || 0,
    job_requirements: job.seniority_level || 'Not specified',
    location_match: calculateLocationMatch(candidate.location, job.location, job.remote_allowed),
    salary_alignment: calculateSalaryAlignment(candidate.salary_expectation, job.salary_min, job.salary_max),
    recommendation: score >= 80 ? 'Excellent match' : 
                   score >= 60 ? 'Good match' : 
                   score >= 40 ? 'Potential match' : 'Poor match'
  }
}

function extractExperienceFromJob(job: any): number {
  const title = job.title?.toLowerCase() || ''
  const description = job.description?.toLowerCase() || ''
  const seniority = job.seniority_level?.toLowerCase() || ''
  
  if (seniority.includes('senior') || title.includes('senior')) return 5
  if (seniority.includes('lead') || title.includes('lead')) return 7
  if (seniority.includes('junior') || title.includes('junior')) return 1
  if (seniority.includes('mid') || title.includes('mid')) return 3
  
  // Extract years from description
  const yearMatch = description.match(/(\d+)\+?\s*years?/i)
  if (yearMatch) return parseInt(yearMatch[1])
  
  return 0 // No specific requirement
}

function calculateLocationScore(candidateLocation: string, jobLocation: string, remoteAllowed: boolean): number {
  if (remoteAllowed) return 15 // Perfect for remote
  if (!candidateLocation || !jobLocation) return 8 // Unknown
  
  const candidate = candidateLocation.toLowerCase()
  const job = jobLocation.toLowerCase()
  
  if (candidate === job) return 15 // Exact match
  if (candidate.includes(job) || job.includes(candidate)) return 12 // Partial match
  
  return 5 // Different locations
}

function calculateLocationMatch(candidateLocation: string, jobLocation: string, remoteAllowed: boolean): string {
  if (remoteAllowed) return 'Remote work available'
  if (!candidateLocation || !jobLocation) return 'Location unknown'
  
  const candidate = candidateLocation.toLowerCase()
  const job = jobLocation.toLowerCase()
  
  if (candidate === job) return 'Perfect location match'
  if (candidate.includes(job) || job.includes(candidate)) return 'Similar location'
  
  return 'Different locations'
}

function calculateSalaryScore(expectation: number, minSalary: number, maxSalary: number): number {
  if (!expectation || (!minSalary && !maxSalary)) return 5 // Unknown
  
  const jobMid = minSalary && maxSalary ? (minSalary + maxSalary) / 2 : (minSalary || maxSalary)
  if (!jobMid) return 5
  
  const diff = Math.abs(expectation - jobMid) / jobMid
  
  if (diff <= 0.1) return 10 // Within 10%
  if (diff <= 0.2) return 8  // Within 20%
  if (diff <= 0.3) return 6  // Within 30%
  
  return 3 // Significant difference
}

function calculateSalaryAlignment(expectation: number, minSalary: number, maxSalary: number): string {
  if (!expectation || (!minSalary && !maxSalary)) return 'Salary not specified'
  
  if (minSalary && maxSalary) {
    if (expectation >= minSalary && expectation <= maxSalary) {
      return 'Expectation within range'
    }
    if (expectation < minSalary) {
      return 'Expectation below range'
    }
    return 'Expectation above range'
  }
  
  const jobSalary = minSalary || maxSalary
  const diff = ((expectation - jobSalary) / jobSalary) * 100
  
  if (Math.abs(diff) <= 10) return 'Well aligned'
  if (diff > 10) return 'Expects higher salary'
  return 'Expects lower salary'
}