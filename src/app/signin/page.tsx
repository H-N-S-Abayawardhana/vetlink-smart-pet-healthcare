import { Suspense } from "react";
import SigninForm from "../../components/signin/SigninForm";

export default function SigninPage() {
  return (
    <div className="min-h-screen">
      <Suspense fallback={<div>Loading...</div>}>
        <SigninForm />
      </Suspense>
    </div>
  );
}
