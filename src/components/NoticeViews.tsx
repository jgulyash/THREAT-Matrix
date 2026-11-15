import { Go } from '../lib/nav';

export function NotFoundView({ what }: { what: string }) {
  return (
    <div className="notice-view">
      <div className="notice-view-title" data-focus-target tabIndex={-1}>
        Not found
      </div>
      <div className="notice-view-body">
        {what ? (
          <>
            Nothing in this version matches <strong>{what}</strong>.
          </>
        ) : (
          'Nothing in this version matches that address.'
        )}{' '}
        The identifier may be mistyped, or it may belong to a different version.
      </div>
      <Go className="adv-back" to="/">
        ← Back to overview
      </Go>
    </div>
  );
}

export function ReservedActorView({ actorId, reason }: { actorId: string; reason: string }) {
  return (
    <div className="notice-view">
      <div className="notice-view-title" data-focus-target tabIndex={-1}>
        {actorId} is a reserved identifier
      </div>
      <div className="notice-view-body">
        This identifier is held so that it is never reused. It has no profile and is not counted
        among the actor profiles.{reason ? ` ${reason}` : ''}
      </div>
      <Go className="adv-back" to="/actors">
        ← All Profiles
      </Go>
    </div>
  );
}
