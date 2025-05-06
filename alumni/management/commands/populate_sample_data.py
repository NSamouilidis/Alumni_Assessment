import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from alumni.models import School, AlumniProfile, Event


class Command(BaseCommand):
    help = 'Populates the database with sample data for testing and demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate sample data...')
        
        # Create schools
        self.create_schools()
        
        # Create sample alumni profiles
        self.create_alumni()
        
        # Create sample events
        self.create_events()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
    
    def create_schools(self):
        schools_data = [
            {
                'name': 'School of Business',
                'description': 'The School of Business offers undergraduate and postgraduate programs in Business Administration, Marketing, Finance, and Human Resource Management. Our programs prepare students for successful careers in the global business environment through practical learning and industry connections.'
            },
            {
                'name': 'School of Computing',
                'description': 'The School of Computing provides cutting-edge education in Computer Science, Software Engineering, Data Science, and Cybersecurity. Our curriculum combines theoretical knowledge with hands-on experience to prepare students for the rapidly evolving tech industry.'
            },
            {
                'name': 'School of Psychology',
                'description': 'The School of Psychology offers comprehensive programs in Psychology, Counseling, and Behavioral Sciences. Our approach integrates research, clinical practice, and community engagement to develop skilled professionals who can address mental health challenges.'
            },
            {
                'name': 'School of Engineering',
                'description': 'The School of Engineering delivers innovative programs in Civil, Mechanical, Electrical, and Environmental Engineering. Our students develop strong technical foundations and problem-solving skills through project-based learning and industry partnerships.'
            },
            {
                'name': 'School of Health Sciences',
                'description': 'The School of Health Sciences provides education in Nursing, Physiotherapy, Nutrition, and Public Health. We combine theoretical knowledge with clinical practice to prepare compassionate and skilled healthcare professionals.'
            }
        ]
        
        for school_data in schools_data:
            School.objects.get_or_create(
                name=school_data['name'],
                defaults={'description': school_data['description']}
            )
            self.stdout.write(f"Created school: {school_data['name']}")
    
    def create_alumni(self):
        # Get all schools
        schools = list(School.objects.all())
        
        # Sample data for alumni
        first_names = ['Alexander', 'Sophia', 'Michael', 'Emma', 'Nicholas', 'Olivia', 
                       'George', 'Isabella', 'John', 'Maria', 'Andreas', 'Christina', 
                       'Dimitris', 'Elena', 'Kostas', 'Anna']
        
        last_names = ['Papadopoulos', 'Georgiou', 'Nikolaou', 'Demetriou', 'Ioannou', 
                      'Konstantinou', 'Antoniou', 'Papas', 'Smith', 'Johnson', 
                      'Williams', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore']
        
        companies = ['Tech Innovations Ltd', 'Global Finance Group', 'Healthcare Solutions', 
                     'Educational Services Inc', 'Engineering Experts', 'Creative Designs', 
                     'Data Analytics Co', 'Sustainable Energy', 'International Trade', 'Marketing Wizards']
        
        job_titles = ['Software Engineer', 'Financial Analyst', 'Project Manager', 
                      'Marketing Specialist', 'HR Consultant', 'Operations Director', 
                      'Research Scientist', 'Data Analyst', 'Product Manager', 'CEO']
        
        degrees = ['BSc', 'BA', 'MSc', 'MA', 'PhD', 'MBA']
        
        majors_by_school = {
            'School of Business': ['Business Administration', 'Marketing', 'Finance', 
                                  'Economics', 'Human Resources', 'International Business'],
            'School of Computing': ['Computer Science', 'Software Engineering', 'Data Science', 
                                   'Information Technology', 'Cybersecurity', 'Artificial Intelligence'],
            'School of Psychology': ['Psychology', 'Clinical Psychology', 'Counseling', 
                                    'Behavioral Science', 'Child Psychology', 'Neuropsychology'],
            'School of Engineering': ['Civil Engineering', 'Mechanical Engineering', 'Electrical Engineering', 
                                     'Environmental Engineering', 'Chemical Engineering', 'Biomedical Engineering'],
            'School of Health Sciences': ['Nursing', 'Physiotherapy', 'Nutrition', 
                                         'Public Health', 'Health Management', 'Medical Laboratory Science']
        }
        
        # Create 20 sample alumni (4 for each school)
        for i in range(20):
            # Select a school
            school = schools[i % len(schools)]
            
            # Create user
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@example.com"
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                username = f"{username}{random.randint(1000, 9999)}"
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',  # Simple password for demo purposes
                first_name=first_name,
                last_name=last_name
            )
            
            # Get random major for the school
            majors = majors_by_school.get(school.name, ['General Studies'])
            
            # Create profile
            status = 'registered' if i < 15 else 'applied'  # 15 registered, 5 applied
            grad_year = random.randint(2010, 2023)
            
            profile = AlumniProfile.objects.get(user=user)
            profile.school = school
            profile.status = status
            profile.date_of_birth = timezone.now().date() - timedelta(days=365*random.randint(25, 40))
            profile.gender = random.choice(['M', 'F', 'O'])
            profile.bio = f"Alumni from {school.name} with expertise in {random.choice(majors)}. Graduated in {grad_year}."
            profile.phone_number = f"+30 69{random.randint(10000000, 99999999)}"
            profile.address = f"Athens, Greece"
            profile.graduation_year = grad_year
            profile.degree = random.choice(degrees)
            profile.major = random.choice(majors)
            profile.current_company = random.choice(companies)
            profile.job_title = random.choice(job_titles)
            profile.linkedin_profile = f"https://linkedin.com/in/{username}"
            profile.save()
            
            self.stdout.write(f"Created alumni: {first_name} {last_name} ({status})")
    
    def create_events(self):
        event_titles = [
            'Annual Alumni Reunion',
            'Career Networking Mixer',
            'Professional Development Workshop',
            'Industry Panel Discussion',
            'Homecoming Celebration',
            'Leadership Symposium',
            'Entrepreneurship Conference',
            'Alumni Awards Gala',
            'Mentorship Program Kickoff',
            'Mediterranean College Anniversary Celebration'
        ]
        
        locations = [
            'Mediterranean College Main Campus, Athens',
            'Grand Hotel Conference Center, Athens',
            'Mediterranean College Thessaloniki Campus',
            'Innovation Hub, Athens Tech Park',
            'Cultural Center, Downtown Athens',
            'Mediterranean College Alumni Lounge',
            'National Conference Center, Athens',
            'Mediterranean Business School Auditorium',
            'Olympic Hotel Ballroom, Athens',
            'Digital Learning Center, Mediterranean College'
        ]
        
        # Create 10 events (5 past, 5 upcoming)
        now = timezone.now()
        
        for i in range(10):
            is_past = i < 5
            
            # Set date (past or future)
            if is_past:
                days_offset = random.randint(30, 365)  # Past event (30 days to 1 year ago)
                event_date = now - timedelta(days=days_offset)
            else:
                days_offset = random.randint(30, 365)  # Future event (30 days to 1 year in future)
                event_date = now + timedelta(days=days_offset)
            
            # Registration deadline (7 days before event)
            registration_deadline = event_date - timedelta(days=7)
            
            # Create event
            event = Event.objects.create(
                title=event_titles[i],
                description=f"Join us for the {event_titles[i]} event! This is a great opportunity for alumni to connect, network, and learn from each other. The event will feature guest speakers, workshops, and networking sessions designed to enhance your professional development and strengthen your connection to the Mediterranean College community.",
                date=event_date,
                location=locations[i],
                registration_required=True,
                registration_deadline=registration_deadline
            )
            
            # Add some registered alumni to past events
            if is_past:
                registered_alumni = AlumniProfile.objects.filter(status='registered').order_by('?')[:random.randint(5, 15)]
                for alumni in registered_alumni:
                    event.attendees.add(alumni)
            
            self.stdout.write(f"Created event: {event_titles[i]} ({event_date.strftime('%Y-%m-%d')})")