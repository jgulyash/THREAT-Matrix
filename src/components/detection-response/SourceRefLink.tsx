interface Props {
  refKey: string;
  navigate: (path: string) => void;
}

export function SourceRefLink({ refKey, navigate }: Props) {
  return (
    <a
      className="dr-tag source-link"
      href="#/references"
      onClick={(e) => {
        e.preventDefault();
        navigate('/references');
        setTimeout(() => {
          const el = document.getElementById(`bib-${refKey}`);
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
      }}
      title={`Source: ${refKey}`}
    >
      {refKey}
    </a>
  );
}
