// Growth Accelerator Platform - Workable API Sync Edge Function
// Supabase Edge Function to sync data from Workable API

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
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

    const workableApiKey = Deno.env.get('WORKABLE_API_KEY')
    const workableSubdomain = 'growthacceleratorstaffing'

    if (!workableApiKey) {
      throw new Error('Workable API key not configured')
    }

    // Sync Candidates
    const candidatesResponse = await fetch(
      `https://${workableSubdomain}.workable.com/spi/v3/candidates`,
      {
        headers: {
          'Authorization': `Bearer ${workableApiKey}`,
          'Content-Type': 'application/json',
        },
      }
    )

    if (!candidatesResponse.ok) {
      throw new Error(`Workable API error: ${candidatesResponse.status}`)
    }

    const candidatesData = await candidatesResponse.json()

    // Process and upsert candidates
    for (const candidate of candidatesData.candidates || []) {
      const candidateRecord = {
        workable_id: candidate.id,
        name: candidate.name,
        email: candidate.email,
        phone: candidate.phone,
        skills: candidate.skills || [],
        experience_years: candidate.experience_years,
        location: candidate.location,
        status: 'active',
        applications_count: candidate.applications?.length || 0,
        resume_url: candidate.resume_url,
        linkedin_url: candidate.social_profiles?.find(p => p.type === 'linkedin')?.url,
        portfolio_url: candidate.website,
        availability: candidate.availability,
        notes: candidate.summary,
      }

      // Upsert candidate (insert or update if exists)
      const { error: candidateError } = await supabaseClient
        .from('candidates')
        .upsert(candidateRecord, { 
          onConflict: 'workable_id',
          ignoreDuplicates: false 
        })

      if (candidateError) {
        console.error('Error upserting candidate:', candidateError)
      }
    }

    // Sync Jobs
    const jobsResponse = await fetch(
      `https://${workableSubdomain}.workable.com/spi/v3/jobs`,
      {
        headers: {
          'Authorization': `Bearer ${workableApiKey}`,
          'Content-Type': 'application/json',
        },
      }
    )

    if (!jobsResponse.ok) {
      throw new Error(`Workable Jobs API error: ${jobsResponse.status}`)
    }

    const jobsData = await jobsResponse.json()

    // Process and upsert jobs
    for (const job of jobsData.jobs || []) {
      const jobRecord = {
        workable_id: job.id,
        title: job.title,
        company: job.department || 'Growth Accelerator',
        location: job.location?.location_str,
        description: job.description,
        requirements: job.requirements || [],
        skills_required: job.skills || [],
        salary_min: job.salary?.min,
        salary_max: job.salary?.max,
        employment_type: job.employment_type || 'full-time',
        remote_allowed: job.remote || false,
        status: job.state === 'published' ? 'active' : 'paused',
        applications_count: 0, // Will be updated separately
        department: job.department,
        seniority_level: job.experience,
      }

      // Upsert job
      const { error: jobError } = await supabaseClient
        .from('jobs')
        .upsert(jobRecord, { 
          onConflict: 'workable_id',
          ignoreDuplicates: false 
        })

      if (jobError) {
        console.error('Error upserting job:', jobError)
      }
    }

    // Get final counts
    const { count: candidatesCount } = await supabaseClient
      .from('candidates')
      .select('*', { count: 'exact', head: true })

    const { count: jobsCount } = await supabaseClient
      .from('jobs')
      .select('*', { count: 'exact', head: true })

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Workable sync completed successfully',
        candidates_synced: candidatesData.candidates?.length || 0,
        jobs_synced: jobsData.jobs?.length || 0,
        total_candidates: candidatesCount,
        total_jobs: jobsCount,
        timestamp: new Date().toISOString(),
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      },
    )

  } catch (error) {
    console.error('Workable sync error:', error)

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