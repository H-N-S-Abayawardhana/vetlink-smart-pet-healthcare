'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Pet } from '@/lib/pets';

interface PetCardProps {
  pet: Pet;
}

export default function PetCard({ pet }: PetCardProps) {
  const router = useRouter();

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' || e.key === ' ') {
      router.push(`/dashboard/pets/${pet.id}`);
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => router.push(`/dashboard/pets/${pet.id}`)}
      onKeyDown={handleKeyDown}
      className="bg-white rounded-lg shadow border border-gray-200 p-4 flex items-center space-x-4 cursor-pointer hover:shadow-md focus:shadow-md"
    >
      <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
        { (pet as any).avatarDataUrl || (pet as any).avatarUrl ? (
          <img src={(pet as any).avatarDataUrl || (pet as any).avatarUrl} alt={`${pet.name} photo`} className="w-full h-full object-cover" />
        ) : (
          <span className="text-xl">🐕</span>
        )}
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">{pet.name}</p>
        <p className="text-sm text-gray-500 truncate">{pet.breed} • {pet.ageYears ? `${pet.ageYears} yrs` : '—'}</p>
      </div>

      <div className="flex items-center">
        <Link
          href={`/dashboard/pets/${pet.id}`}
          onClick={(e) => e.stopPropagation()}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          Edit
        </Link>
      </div>
    </div>
  );
}
