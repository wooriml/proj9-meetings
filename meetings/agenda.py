"""
Edited for optimization for CIS322 proj8-freetimes
author: CIS210
Edit: Jenny Lee

no need for datetime importation.
"""

class Appt:
    def __init__(self, begin, end):

        self._begin = begin
        self._end = end

    def __repr__(self):
        """returns str representation of self._begin and self._end
        alternative way instead of __str__(self)
        """
        return (self._begin + " to " + self._end)


    def __lt__(self, other):
        """Does this appointment finish before other begins?
        
        Arguments:
        	other: another Appt
        Returns: 
        	True iff this Appt is done by the time other begins.
        """
        return self._end <= other._begin
        
    def __gt__(self, other):
        """Does other appointment finish before this begins?
        
        Arguments:
        	other: another Appt
        Returns: 
        	True iff other is done by the time this Appt begins
        """
        return other < self
        
    def overlaps(self, other):
        """Is there a non-zero overlap between this appointment
        and the other appointment?
		Arguments:
            other is an Appt
        Returns:
            True iff there exists some duration (greater than zero)
            between this Appt and other. 
        """
        return  not (self < other or other < self)
            
    def intersect(self, other):
        """Return an appointment representing the period in
        common between this appointment and another.
        Requires self.overlaps(other).
        
		Arguments: 
			other:  Another Appt

		Returns: 
			An appointment representing the time period in common
			between self and other.   Description of returned Appt 
			is copied from this (self), unless a non-null string is 
			provided as desc. 
        """
        #if desc=="":
         #   desc = self.desc
        assert(self.overlaps(other))

        begin_time = max(self._begin, other._begin)
        end_time = min(self._end, other._end)
        return Appt(begin_time, end_time)

    def union(self, other):
        """Return an appointment representing the combined period in
        common between this appointment and another.
        Requires self.overlaps(other).
        
		Arguments: 
			other:  Another Appt

		Returns: 
			An appointment representing the time period spanning
                        both self and other.   Description of returned Appt 
			is concatenation of two unless a non-null string is 
			provided as desc. 
        """
        #if desc=="":
        #    desc = self.desc + " " + other.desc
        assert(self.overlaps(other))

        begin = min(self._begin, other._begin)
        end = max(self.end, other.end)
        return Appt(begin, end)

    """
    _str_ is alternated with _repr_
    def __str__(self):
        String representation of appointment.
        Example:
            2012.10.31 13:00 13:50 | CIS 210 lecture
            
        This format is designed to be easily divided
        into parts:  Split on '|', then split on whitespace,
        then split date on '.' and times on ':'.
        
        daystr = self.begin.date().strftime("%Y.%m.%d ")
        begstr = self.begin.strftime("%H:%M ")
        endstr = self.end.strftime("%H:%M ")
        return daystr + begstr + endstr + "| " + self.desc
    """





class Agenda:
    """An Agenda is essentially a list of appointments,
    with some agenda-specific methods.
    """

    def __init__(self):
        """An empty agenda."""
        self._appts = [ ]
    
    def listf(self):
        return self._appts
    
    def append(self,appt):
        """Add an Appt to the agenda."""
        self.appts.append(appt)

    def intersect(self,other): 
        """Return a new agenda containing appointments
        that are overlaps between appointments in this agenda
        and appointments in the other agenda.

        Arguments:
           other: Another Agenda, to be intersected with this one
        """
        #default_desc = (desc == "")
        result = Agenda()
        for thisappt in self._appts:
            for otherappt in other._appts:
                if thisappt.overlaps(otherappt):
                    result.append(thisappt.intersect(otherappt))
        
        return result

    def normalize(self):
        """Merge overlapping events in an agenda. For example, if 
        the first appointment is from 1pm to 3pm, and the second is
        from 2pm to 4pm, these two are merged into an appt from 
        1pm to 4pm, with a combination description.  
        After normalize, the agenda is in order by date and time, 
        with no overlapping appointments.
        """
        if len(self.appts) == 0:
            return

        ordering = lambda ap: ap._begin
        self.appts.sort(key=ordering)

        normalized = [ ]
        print("Starting normalization")
        cur = self._appts[0]  
        for appt in self._appts[1:]:
            if appt > cur:
                # Not overlapping
                # print("Gap - emitting ", cur)
                normalized.append(cur)
                cur = appt
            else:
                # Overlapping
                # print("Merging ", cur, "\n"+
                #      "with    ", appt)
                cur = cur.union(appt)
                # print("New cur: ", cur)
        # print("Last appt: ", cur)
        normalized.append(cur)
        self._appts = normalized

    def normalized(self):
        """
        A non-destructive normalize
        (like "sorted(l)" vs "l.sort()").
        Returns a normalized copy of this agenda.
        """
        copy = Agenda()
        copy._appts = self._appts
        copy.normalize()
        return copy
        
    def complement(self, freeblock):
        """Produce the complement of an agenda
        within the span of a timeblock represented by 
        an appointment.  For example, 
        if this agenda is a set of appointments, produce a 
        new agenda of the times *not* in appointments in 
        a given time period.
        Args: 
           freeblock: Looking  for time blocks in this period 
               that are not conflicting with appointments in 
               this agenda.
        Returns: 
           A new agenda containing exactly the times that 
           are within the period of freeblock and 
           not within appointments in this agenda. The 
           description of the resulting appointments comes
           from freeblock.desc.
        """
        copy = self.normalized()
        comp = Agenda()
        
        cur_time = freeblock._begin

        for appt in copy._appts:
            if appt < freeblock:
                continue
            if appt > freeblock:
                if cur_time < freeblock._end:
                    comp.append(Appt(cur_time,freeblock._end))
                    cur_time = freeblock._end
                break
            if cur_time < appt._begin:
                comp.append(Appt(cur_time, appt._begin))
            cur_time = max(appt._end,cur_time)
        if cur_time < freeblock._end:
            comp.append(Appt(cur_time, freeblock._end))
        return comp

    def appendation(self):
        """append dictionary by iteration with the readable object
        """
        res = []
        for appt in self._appts:
            res.append({"startingtime": appt._begin.format("MM/DD.YYYY HH:mm"),
                        "endingtime": appt._end.format("MM/DD/YYYY HH:mm")})
        return res


    def __len__(self):
        """Number of appointments, callable as built-in len() function"""
        return len(self.appts)

    def __iter__(self):
        """An iterator through the appointments in this agenda."""
        return self.appts.__iter__()


