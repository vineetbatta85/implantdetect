import React from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, Eye } from "lucide-react";

const parts = [
  {
    name: "Hip",
    color: "bg-indigo-100",
    hoverColor: "hover:bg-indigo-200",
    borderColor: "border-indigo-300",
    textColor: "text-indigo-800",
    to: "/xray/hip",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-13-at-12.48.33-am.jpeg",
    description: "Total hip replacements, hip resurfacing, and acetabular components",
    count: "11 implants"
  },
  {
    name: "Knee",
    color: "bg-purple-100",
    hoverColor: "hover:bg-purple-200",
    borderColor: "border-purple-300",
    textColor: "text-purple-800",
    to: "/xray/knee",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/vanguard-1.png",
    description: "Total knee replacements, unicondylar, and patellofemoral implants",
    count: "12 implants"
  },
  {
    name: "Shoulder",
    color: "bg-pink-100",
    hoverColor: "hover:bg-pink-200",
    borderColor: "border-pink-300",
    textColor: "text-pink-800",
    to: "/xray/shoulder", 
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/3m-ap-2.png",
    description: "Total shoulder, reverse shoulder, and hemiarthroplasty implants",
    count: "21 implants"
  },
  {
    name: "Wrist",
    color: "bg-green-100",
    hoverColor: "hover:bg-green-200",
    borderColor: "border-green-300",
    textColor: "text-green-800",
    to: "/xray/wrist",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-07-12-at-8.29.51-am.jpeg",
    description: "Wrist replacement systems and arthroplasty implants",
    count: "11 implants"
  },
  {
    name: "Spine",
    color: "bg-blue-100",
    hoverColor: "hover:bg-blue-200",
    borderColor: "border-blue-300",
    textColor: "text-blue-800",
    to: "/xray/spine",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-14-at-11.42.53-pm.jpeg",
    description: "Cervical, thoracic, and lumbar spinal fixation systems",
    count: "15 implants"
  },
  {
    name: "Ankle",
    color: "bg-teal-100",
    hoverColor: "hover:bg-teal-200",
    borderColor: "border-teal-300",
    textColor: "text-teal-800",
    to: "/xray/ankle",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-15-at-2.37.52-am.jpeg",
    description: "Total ankle replacements and arthrodesis implants",
    count: "8 implants"
  },
  {
    name: "Foot",
    color: "bg-yellow-100",
    hoverColor: "hover:bg-yellow-200",
    borderColor: "border-yellow-300",
    textColor: "text-yellow-800",
    to: "/xray/foot",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-15-at-2.37.52-am.jpeg",
    description: "Forefoot, midfoot, and hindfoot implant systems",
    count: "9 implants"
  },
  {
    name: "Thumb",
    color: "bg-red-100",
    hoverColor: "hover:bg-red-200",
    borderColor: "border-red-300",
    textColor: "text-red-800",
    to: "/xray/thumb",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-14-at-10.30.28-pm.jpeg",
    description: "Thumb joint replacements and CMC arthroplasty implants",
    count: "6 implants"
  },
  {
    name: "Elbow",
    color: "bg-orange-100",
    hoverColor: "hover:bg-orange-200",
    borderColor: "border-orange-300",
    textColor: "text-orange-800",
    to: "/xray/elbow",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-15-at-2.35.29-am-e1757884077286.jpeg",
    description: "Total elbow arthroplasty and radial head prostheses",
    count: "7 implants"
  },
  {
    name: "Finger",
    color: "bg-cyan-100",
    hoverColor: "hover:bg-cyan-200",
    borderColor: "border-cyan-300",
    textColor: "text-cyan-800",
    to: "/xray/finger",
    image: "https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-14-at-10.32.04-pm.jpeg",
    description: "Finger joint prostheses and arthroplasty implants",
    count: "5 implants"
  }
];

const XrayLibrary = () => {
  const navigate = useNavigate();

  const handleNavigate = (to: string) => {
    navigate(to);
  };

  const handleBack = () => {
    navigate('/implant-identification');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleBack}
                className="flex items-center space-x-2 text-gray-600 hover:text-blue-600 transition-colors duration-200 group"
              >
                <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform duration-200" />
                <span className="font-medium">Back to Main</span>
              </button>
              <div className="h-6 w-px bg-gray-300"></div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">X-ray Implant Library</h1>
                <p className="text-gray-600 mt-1">Select an implant category to browse X-ray images</p>
              </div>
            </div>

            {/* Stats */}
           <div className="hidden md:flex items-center space-x-6 text-sm">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600"></div>
                <div className="text-gray-500">Total Implants</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{parts.length}</div>
                <div className="text-gray-500">Categories</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {parts.map((part) => (
            <div
              key={part.name}
              onClick={() => handleNavigate(part.to)}
              className={`group cursor-pointer bg-white rounded-2xl shadow-md hover:shadow-2xl 
                         transition-all duration-500 ease-out hover:scale-105 overflow-hidden
                         border-2 ${part.borderColor} ${part.hoverColor}`}
            >
              {/* Image */}
              <div className="relative h-64 overflow-hidden">
                <img
                  src={part.image}
                  alt={`${part.name} X-ray implant`}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                <div className="absolute top-4 right-4 bg-white/20 backdrop-blur-sm rounded-full p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <Eye className="w-5 h-5 text-white" />
                </div>
                <div className="absolute bottom-4 left-4">
                  <span className="bg-white/90 backdrop-blur-sm text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
                    {part.count}
                  </span>
                </div>
              </div>

              {/* Content */}
              <div className={`p-6 ${part.color}`}>
                <div className="flex items-center justify-between mb-3">
                  <h2 className={`text-2xl font-bold ${part.textColor} group-hover:text-opacity-80 transition-colors duration-300`}>
                    {part.name} Implants
                  </h2>
                  <ArrowRight className={`w-6 h-6 ${part.textColor} group-hover:translate-x-2 transition-transform duration-300`} />
                </div>
                <p className="text-gray-700 text-sm leading-relaxed mb-4">{part.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className="px-2 py-1 bg-white/60 text-gray-700 text-xs font-medium rounded-md">X-ray Images</span>
                  <span className="px-2 py-1 bg-white/60 text-gray-700 text-xs font-medium rounded-md">3D Models</span>
                  <span className="px-2 py-1 bg-white/60 text-gray-700 text-xs font-medium rounded-md">Specifications</span>
                </div>
                <button className={`w-full ${part.textColor} font-semibold py-3 px-4 rounded-lg bg-white/80 hover:bg-white transition-all duration-200 flex items-center justify-center space-x-2 group-hover:shadow-md`}>
                  <span>Browse {part.name} Implants</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default XrayLibrary;

