import { createContext, useContext, type AnchorHTMLAttributes, type ReactNode } from 'react';
import { hrefFor, type Filters } from './route';

// Active filters, shared so every in-app link can carry them.
export const FilterContext = createContext<Filters>({ mode: '', actor: '' });

export const useFilters = (): Filters => useContext(FilterContext);

interface GoProps extends Omit<AnchorHTMLAttributes<HTMLAnchorElement>, 'href'> {
  to: string;
  children: ReactNode;
}

// In-app navigation is always a real link: keyboard reachable, focusable,
// and usable with middle-click or copy-link. The hash router needs no click
// handler.
export function Go({ to, children, ...rest }: GoProps) {
  const filters = useFilters();
  return (
    <a href={hrefFor(to, filters)} {...rest}>
      {children}
    </a>
  );
}
