import React from 'react';
import { Linkedin, Mail, Award, GraduationCap } from 'lucide-react';

const Team = () => {
  const founder = {
    name: "Mr Vineet Batta",
    title: "Founder",
    image: "",
    bio: "Orthopaedic Surgeon , Luton & Dunstable University Hospital NHS Trust, UK Honorary Lecturer ,Department of Bioengineering and Surgical Technology ,Royal National Orthopaedic Hospital Stanmore, UCL, UK",
    education: "MBBS,MS(Trauma),Dip Sports Med,FRCS (Orth),MD(Ortho Research & Bio Med Eng.)",
    linkedin: "#",
    email: "sarah.johnson@aiimaging.com"
  };

  const technicalAdvisor = {
    name: "Dr. Michael Chen",
    title: "Chief Technical Advisor",
    image: "https://images.pexels.com/photos/5452293/pexels-photo-5452293.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&dpr=2",
    bio: "AI researcher specializing in medical imaging and deep learning. Former lead scientist at Google DeepMind Health division.",
    education: "PhD Computer Science, Stanford University",
    linkedin: "#",
    email: "michael.chen@aiimaging.com"
  };

  const advisoryBoard = [
    {
      name: "Dr. Emily Rodriguez",
      title: "Orthopedic Surgery Advisor",
      image: "https://images.pexels.com/photos/5452268/pexels-photo-5452268.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&dpr=2",
      bio: "Senior orthopedic surgeon at Mayo Clinic with expertise in complex joint replacements and revision surgeries.",
      linkedin: "#"
    },
    {
      name: "Dr. James Thompson",
      title: "Radiology Advisor",
      image: "https://images.pexels.com/photos/5452274/pexels-photo-5452274.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&dpr=2",
      bio: "Chief of Radiology at Johns Hopkins Hospital, specializing in musculoskeletal imaging and interventional radiology.",
      linkedin: "#"
    },
    {
      name: "Dr. Lisa Park",
      title: "AI Ethics Advisor",
      image: "https://images.pexels.com/photos/5452299/pexels-photo-5452299.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&dpr=2",
      bio: "Professor of Medical Ethics and AI Policy at Stanford University. Expert in healthcare AI governance and patient privacy.",
      linkedin: "#"
    }
  ];

  const mentors = [
    {
      name: "Prof. Robert Williams",
      title: "Industry Mentor",
      image: "https://images.pexels.com/photos/5452297/pexels-photo-5452297.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&dpr=2",
      bio: "Former CEO of MedTech Solutions. 25+ years of experience in healthcare technology commercialization.",
      linkedin: "#"
    },
    {
      name: "Dr. Amanda Foster",
      title: "Research Mentor",
      image: "https://images.pexels.com/photos/5452290/pexels-photo-5452290.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&dpr=2",
      bio: "Director of Biomedical Engineering at MIT. Pioneer in medical device innovation and translational research.",
      linkedin: "#"
    }
  ];

  const TeamCard = ({ member, isFounder = false, showEmail = false }) => (
    <div className={`bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 ${isFounder ? 'md:col-span-2' : ''}`}>
      <div className="p-6">
        <div className="flex flex-col items-center text-center">
          <div className="w-32 h-32 mb-4 overflow-hidden rounded-full border-4 border-gradient-to-r from-primary-500 to-emerald-500">
            <img
              src={member.image}
              alt={member.name}
              className="w-full h-full object-cover"
            />
          </div>
          
          <h3 className="text-xl font-bold text-gray-900 mb-1">{member.name}</h3>
          <p className="text-primary-600 font-semibold mb-3">{member.title}</p>
          
          {member.education && (
            <div className="flex items-center text-sm text-gray-600 mb-3">
              <GraduationCap className="w-4 h-4 mr-1" />
              <span>{member.education}</span>
            </div>
          )}
          
          <p className="text-gray-600 text-sm mb-4 leading-relaxed">
            {member.bio}
          </p>
          
          <div className="flex space-x-3">
            <a
              href={member.linkedin}
              className="p-2 bg-primary-50 text-primary-600 rounded-lg hover:bg-primary-100 transition-colors duration-200"
            >
              <Linkedin className="w-5 h-5" />
            </a>
            {showEmail && (
              <a
                href={`mailto:${member.email}`}
                className="p-2 bg-emerald-50 text-emerald-600 rounded-lg hover:bg-emerald-100 transition-colors duration-200"
              >
                <Mail className="w-5 h-5" />
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
            Meet Our Team
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            A diverse group of medical professionals, AI researchers, and industry experts united by a vision to transform surgical care through intelligent technology.
          </p>
        </div>

        {/* Founder Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Founder</h2>
            <p className="text-lg text-gray-600">
              Visionary leadership driving innovation in medical AI
            </p>
          </div>
          
          <div className="max-w-2xl mx-auto">
            <TeamCard member={founder} showEmail={true} />
          </div>
        </section>

        {/* Technical Advisor Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Technical Advisor</h2>
            <p className="text-lg text-gray-600">
              Technical expertise guiding our AI development
            </p>
          </div>
          
          <div className="max-w-2xl mx-auto">
            <TeamCard member={technicalAdvisor} showEmail={true} />
          </div>
        </section>

        {/* Advisory Board Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Advisory Board</h2>
            <p className="text-lg text-gray-600">
              Expert advisors providing strategic guidance and clinical insights
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {advisoryBoard.map((member, index) => (
              <TeamCard key={index} member={member} />
            ))}
          </div>
        </section>

        {/* Mentors Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Mentors</h2>
            <p className="text-lg text-gray-600">
              Industry veterans providing wisdom and strategic direction
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {mentors.map((member, index) => (
              <TeamCard key={index} member={member} />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Team;
