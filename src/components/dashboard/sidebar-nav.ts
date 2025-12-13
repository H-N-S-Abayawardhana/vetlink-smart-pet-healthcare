import type { ComponentType, SVGProps } from 'react';
import type { UserRole } from '@/types/next-auth';
import {
  HomeIcon,
  HeartIcon,
  DocumentTextIcon,
  CalendarIcon,
  LightBulbIcon,
  EyeIcon,
  CogIcon,
} from '@heroicons/react/24/outline';

export type SidebarIcon = ComponentType<SVGProps<SVGSVGElement>>;

export type SidebarNavPlacement = 'top' | 'bottom';

export interface SidebarNavItem {
  name: string;
  href: string;
  icon: SidebarIcon;
  roles: UserRole[];
  placement?: SidebarNavPlacement;
}

const SIDEBAR_NAV_ITEMS: SidebarNavItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: HomeIcon,
    roles: ['SUPER_ADMIN', 'VETERINARIAN', 'USER'],
  },
  {
    name: 'My Pets',
    href: '/dashboard/pets',
    icon: HeartIcon,
    roles: ['SUPER_ADMIN', 'VETERINARIAN', 'USER'],
  },
  {
    name: 'BCS Calculator',
    href: '/dashboard/pets/bcs',
    icon: LightBulbIcon,
    roles: ['SUPER_ADMIN', 'VETERINARIAN', 'USER'],
  },
  {
    name: 'Diet Recommendations',
    href: '/dashboard/pets/diet',
    icon: DocumentTextIcon,
    roles: ['SUPER_ADMIN', 'VETERINARIAN', 'USER'],
  },
  {
    name: 'Schedule Appointment',
    href: '/dashboard/appointment-schedule',
    icon: CalendarIcon,
    roles: ['USER'],
  },
  {
    name: 'Appointments',
    href: '/dashboard/appointment-schedule',
    icon: CalendarIcon,
    roles: ['SUPER_ADMIN'],
  },
  {
    name: 'Manage Appointments',
    href: '/dashboard/veterinarian-appointments',
    icon: CalendarIcon,
    roles: ['VETERINARIAN'],
  },
  {
    name: 'Skin Disease Detection',
    href: '/dashboard/skin-disease',
    icon: EyeIcon,
    roles: ['SUPER_ADMIN', 'VETERINARIAN', 'USER'],
  },
  {
    name: 'Limping Detection',
    href: '/dashboard/Limping',
    icon: EyeIcon,
    roles: ['SUPER_ADMIN', 'VETERINARIAN'],
  },
  {
    name: 'Settings',
    href: '/dashboard/settings',
    icon: CogIcon,
    roles: ['SUPER_ADMIN'],
    placement: 'bottom',
  },
];

export function getSidebarNavItems(userRole: UserRole): {
  top: SidebarNavItem[];
  bottom: SidebarNavItem[];
} {
  const allowed = SIDEBAR_NAV_ITEMS.filter((item) => item.roles.includes(userRole));
  return {
    top: allowed.filter((item) => (item.placement ?? 'top') === 'top'),
    bottom: allowed.filter((item) => item.placement === 'bottom'),
  };
}


