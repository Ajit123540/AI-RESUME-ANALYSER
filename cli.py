#!/usr/bin/env python3
"""
AI Resume Analyzer CLI Tool
Command-line interface for resume analysis
"""

import click
import json
import os
from pathlib import Path
from typing import List, Optional

from src.analyzer import ResumeAnalyzer


@click.group()
def cli():
    """AI Resume Analyzer - Command-line tool for resume analysis"""
    pass


@cli.command()
@click.option('--resume', '-r', required=True, type=click.Path(exists=True), help='Path to resume file')
@click.option('--job-description', '-j', type=str, help='Job description for matching')
@click.option('--required-skills', '-s', type=str, help='Comma-separated list of required skills')
@click.option('--output', '-o', type=click.Path(), help='Output file for results (JSON)')
@click.option('--no-ai', is_flag=True, help='Disable AI analysis')
def analyze(resume, job_description, required_skills, output, no_ai):
    """Analyze a single resume file"""
    try:
        # Parse required skills
        skills_list = None
        if required_skills:
            skills_list = [skill.strip() for skill in required_skills.split(',')]
        
        # Initialize analyzer
        analyzer = ResumeAnalyzer(use_ai=not no_ai)
        
        # Analyze resume
        click.echo(f"Analyzing resume: {resume}")
        result = analyzer.analyze_file(resume, job_description, skills_list)
        
        # Display results
        display_results(result)
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"\nResults saved to: {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--directory', '-d', required=True, type=click.Path(exists=True), help='Directory containing resume files')
@click.option('--job-description', '-j', type=str, help='Job description for matching')
@click.option('--required-skills', '-s', type=str, help='Comma-separated list of required skills')
@click.option('--output', '-o', type=click.Path(), help='Output file for results (JSON)')
@click.option('--no-ai', is_flag=True, help='Disable AI analysis')
@click.option('--extension', '-e', default='pdf', help='File extension to filter (default: pdf)')
def batch(directory, job_description, required_skills, output, no_ai, extension):
    """Analyze multiple resume files in a directory"""
    try:
        # Parse required skills
        skills_list = None
        if required_skills:
            skills_list = [skill.strip() for skill in required_skills.split(',')]
        
        # Find resume files
        dir_path = Path(directory)
        resume_files = list(dir_path.glob(f"*.{extension}"))
        
        if not resume_files:
            click.echo(f"No .{extension} files found in {directory}")
            return
        
        click.echo(f"Found {len(resume_files)} resume files")
        
        # Initialize analyzer
        analyzer = ResumeAnalyzer(use_ai=not no_ai)
        
        # Batch analyze
        click.echo("Analyzing resumes...")
        results = analyzer.batch_analyze([str(f) for f in resume_files], job_description, skills_list)
        
        # Display summary
        successful = sum(1 for r in results if r.get('parse_success'))
        click.echo(f"\nSuccessfully analyzed: {successful}/{len(resume_files)}")
        
        # Display individual results
        for i, result in enumerate(results, 1):
            click.echo(f"\n--- Resume {i}: {result.get('file_name', 'Unknown')} ---")
            if result.get('parse_success'):
                overall = result.get('overall_assessment', {})
                click.echo(f"Recommendation: {overall.get('recommendation', 'N/A')}")
                click.echo(f"Confidence Score: {overall.get('confidence_score', 0)}%")
                click.echo(f"Skills Found: {result.get('skills_analysis', {}).get('skill_count', 0)}")
                
                if result.get('ai_ranking'):
                    ranking = result['ai_ranking']
                    click.echo(f"AI Rank: #{ranking.get('rank', 'N/A')}")
                    click.echo(f"AI Score: {ranking.get('score', 0)}")
            else:
                click.echo(f"Error: {result.get('error', 'Unknown error')}")
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults saved to: {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--resume', '-r', required=True, type=click.Path(exists=True), help='Path to resume file')
@click.option('--job-description', '-j', required=True, type=str, help='Job description for improvement suggestions')
@click.option('--output', '-o', type=click.Path(), help='Output file for suggestions (JSON)')
def improve(resume, job_description, output):
    """Get AI-powered improvement suggestions for a resume"""
    try:
        # Initialize analyzer
        analyzer = ResumeAnalyzer(use_ai=True)
        
        if not analyzer.use_ai:
            click.echo("Error: AI features not enabled. Set OPENAI_API_KEY environment variable.", err=True)
            raise click.Abort()
        
        # Parse resume
        click.echo(f"Analyzing resume: {resume}")
        resume_text = analyzer.parser.parse_file(resume)
        
        # Get suggestions
        click.echo("Generating improvement suggestions...")
        suggestions = analyzer.get_improvement_suggestions(resume_text, job_description)
        
        # Display suggestions
        click.echo("\n=== IMPROVEMENT SUGGESTIONS ===")
        
        if suggestions.get('error'):
            click.echo(f"Error: {suggestions['error']}", err=True)
        else:
            if suggestions.get('missing_skills'):
                click.echo("\n📚 Missing Skills to Add:")
                for skill in suggestions['missing_skills']:
                    click.echo(f"  • {skill}")
            
            if suggestions.get('experience_gaps'):
                click.echo("\n💼 Experience Gaps to Address:")
                for gap in suggestions['experience_gaps']:
                    click.echo(f"  • {gap}")
            
            if suggestions.get('format_improvements'):
                click.echo("\n📝 Format & Structure Improvements:")
                for improvement in suggestions['format_improvements']:
                    click.echo(f"  • {improvement}")
            
            if suggestions.get('keywords_to_include'):
                click.echo("\n🔑 Keywords to Include:")
                for keyword in suggestions['keywords_to_include']:
                    click.echo(f"  • {keyword}")
            
            if suggestions.get('achievements_to_highlight'):
                click.echo("\n🏆 Achievements to Highlight:")
                for achievement in suggestions['achievements_to_highlight']:
                    click.echo(f"  • {achievement}")
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(suggestions, f, indent=2)
            click.echo(f"\nSuggestions saved to: {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--resume1', '-r1', required=True, type=click.Path(exists=True), help='Path to first resume')
@click.option('--resume2', '-r2', required=True, type=click.Path(exists=True), help='Path to second resume')
@click.option('--job-description', '-j', required=True, type=str, help='Job description for comparison')
@click.option('--output', '-o', type=click.Path(), help='Output file for comparison (JSON)')
def compare(resume1, resume2, job_description, output):
    """Compare two resumes using AI"""
    try:
        # Initialize analyzer
        analyzer = ResumeAnalyzer(use_ai=True)
        
        if not analyzer.use_ai:
            click.echo("Error: AI features not enabled. Set OPENAI_API_KEY environment variable.", err=True)
            raise click.Abort()
        
        # Compare resumes
        click.echo(f"Comparing resumes: {resume1} vs {resume2}")
        comparison = analyzer.compare_resumes(resume1, resume2, job_description)
        
        # Display comparison
        click.echo("\n=== RESUME COMPARISON ===")
        
        if comparison.get('error'):
            click.echo(f"Error: {comparison['error']}", err=True)
        else:
            click.echo(f"\n🏆 Better Resume: {comparison.get('better_resume', 'N/A')}")
            click.echo(f"\n📋 Reasoning: {comparison.get('reasoning', 'N/A')}")
            
            if comparison.get('key_differences'):
                click.echo("\n🔍 Key Differences:")
                for diff in comparison['key_differences']:
                    click.echo(f"  • {diff}")
            
            if comparison.get('resume1_strengths'):
                click.echo(f"\n✅ Resume 1 Strengths:")
                for strength in comparison['resume1_strengths']:
                    click.echo(f"  • {strength}")
            
            if comparison.get('resume1_weaknesses'):
                click.echo(f"\n❌ Resume 1 Weaknesses:")
                for weakness in comparison['resume1_weaknesses']:
                    click.echo(f"  • {weakness}")
            
            if comparison.get('resume2_strengths'):
                click.echo(f"\n✅ Resume 2 Strengths:")
                for strength in comparison['resume2_strengths']:
                    click.echo(f"  • {strength}")
            
            if comparison.get('resume2_weaknesses'):
                click.echo(f"\n❌ Resume 2 Weaknesses:")
                for weakness in comparison['resume2_weaknesses']:
                    click.echo(f"  • {weakness}")
            
            click.echo(f"\n📝 Final Recommendation: {comparison.get('final_recommendation', 'N/A')}")
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(comparison, f, indent=2)
            click.echo(f"\nComparison saved to: {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--text', '-t', required=True, type=str, help='Resume text to analyze')
@click.option('--job-description', '-j', type=str, help='Job description for matching')
@click.option('--required-skills', '-s', type=str, help='Comma-separated list of required skills')
@click.option('--output', '-o', type=click.Path(), help='Output file for results (JSON)')
@click.option('--no-ai', is_flag=True, help='Disable AI analysis')
def analyze_text(text, job_description, required_skills, output, no_ai):
    """Analyze resume text directly"""
    try:
        # Parse required skills
        skills_list = None
        if required_skills:
            skills_list = [skill.strip() for skill in required_skills.split(',')]
        
        # Initialize analyzer
        analyzer = ResumeAnalyzer(use_ai=not no_ai)
        
        # Analyze text
        click.echo("Analyzing resume text...")
        result = analyzer.analyze_resume(text, job_description, skills_list)
        
        # Display results
        display_results(result)
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"\nResults saved to: {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


def display_results(result):
    """Display analysis results in a formatted way"""
    if not result.get('parse_success'):
        click.echo(f"❌ Error: {result.get('error', 'Unknown error')}", err=True)
        return
    
    click.echo("\n" + "="*50)
    click.echo("📊 RESUME ANALYSIS RESULTS")
    click.echo("="*50)
    
    # Overall assessment
    overall = result.get('overall_assessment', {})
    if overall:
        click.echo(f"\n🎯 Overall Assessment")
        click.echo(f"   Recommendation: {overall.get('recommendation', 'N/A')}")
        click.echo(f"   Confidence Score: {overall.get('confidence_score', 0)}%")
        
        if overall.get('strengths'):
            click.echo(f"\n   ✅ Strengths:")
            for strength in overall['strengths']:
                click.echo(f"      • {strength}")
        
        if overall.get('weaknesses'):
            click.echo(f"\n   ❌ Weaknesses:")
            for weakness in overall['weaknesses']:
                click.echo(f"      • {weakness}")
    
    # Skills analysis
    skills = result.get('skills_analysis', {})
    if skills:
        click.echo(f"\n📚 Skills Analysis")
        click.echo(f"   Total Skills Found: {skills.get('skill_count', 0)}")
        
        if skills.get('categorized'):
            for category, skill_list in skills['categorized'].items():
                click.echo(f"   {category}: {', '.join(skill_list)}")
    
    # Keyword matching
    keywords = result.get('keyword_matching', {})
    if keywords and keywords.get('combined_score') is not None:
        click.echo(f"\n🔑 Keyword Matching")
        click.echo(f"   Combined Score: {keywords.get('combined_score', 0)}%")
        click.echo(f"   Keyword Score: {keywords.get('keyword_score', 0)}%")
        click.echo(f"   Phrase Score: {keywords.get('phrase_score', 0)}%")
        
        if keywords.get('matched_keywords'):
            click.echo(f"   Matched Keywords: {', '.join(keywords['matched_keywords'])}")
        
        if keywords.get('missing_keywords'):
            click.echo(f"   Missing Keywords: {', '.join(keywords['missing_keywords'])}")
    
    # Skills comparison
    skills_comp = result.get('skills_comparison', {})
    if skills_comp:
        click.echo(f"\n📊 Skills Comparison")
        click.echo(f"   Match Percentage: {skills_comp.get('match_percentage', 0)}%")
        click.echo(f"   Matched: {skills_comp.get('total_matched', 0)}/{skills_comp.get('total_required', 0)}")
        
        if skills_comp.get('matched_skills'):
            click.echo(f"   Matched Skills: {', '.join(skills_comp['matched_skills'])}")
        
        if skills_comp.get('missing_skills'):
            click.echo(f"   Missing Skills: {', '.join(skills_comp['missing_skills'])}")
    
    # AI analysis
    ai = result.get('ai_analysis', {})
    if ai and not ai.get('error'):
        click.echo(f"\n🤖 AI Analysis")
        click.echo(f"   AI Score: {ai.get('overall_score', 0)}/100")
        click.echo(f"   Recommendation: {ai.get('recommendation', 'N/A')}")
        click.echo(f"   Summary: {ai.get('summary', 'N/A')}")
        click.echo(f"   Skill Match: {ai.get('skill_match', 'N/A')}")
        click.echo(f"   Experience Relevance: {ai.get('experience_relevance', 'N/A')}")
        
        if ai.get('strengths'):
            click.echo(f"   AI Strengths: {', '.join(ai['strengths'])}")
        
        if ai.get('weaknesses'):
            click.echo(f"   AI Weaknesses: {', '.join(ai['weaknesses'])}")
    
    # Resume stats
    click.echo(f"\n📄 Resume Statistics")
    click.echo(f"   Text Length: {result.get('resume_text_length', 0)} characters")
    click.echo(f"   Word Count: {result.get('word_count', 0)} words")
    
    click.echo("\n" + "="*50)


if __name__ == '__main__':
    cli()
