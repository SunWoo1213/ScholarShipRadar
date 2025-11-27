import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "장학금 레이더 - 맞춤형 장학금 찾기",
  description: "대학생을 위한 맞춤형 장학금 검색 플랫폼",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}

