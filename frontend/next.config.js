/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Example of a more advanced configuration:
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: 'http://localhost:5000/api/:path*', // Proxy to Backend
  //     },
  //   ]
  // },
};

module.exports = nextConfig;
