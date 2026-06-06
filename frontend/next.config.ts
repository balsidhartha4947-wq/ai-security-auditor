import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://unrobed-wrongdoer-splotchy.ngrok-free.dev/:path*",
      },
    ];
  },
};

export default nextConfig;